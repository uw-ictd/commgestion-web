#! /usr/bin/env python

"""Generates fake data on the traffic detection function (TDF) interface

This module implements a client which generates realistic fake data and
reports it over the TDF interface to the core logging subsystem.
"""

import cbor2
import datetime
import random
import requests
import threading


class UsageGenerator(object):
    """Generates a random walk of measurements with configurable step variation

    Tracks usage as an integer rather than a float
    """
    def __init__(self,
                 baseline_usage,
                 max_step_variation,
                 clamp_min=None,
                 clamp_max=None):
        self._current_usage = baseline_usage
        self._variation = max_step_variation
        self._clamp_min = clamp_min
        self._clamp_max = clamp_max

    def take_step(self):
        """Take a step in the random walk

        :return the sample after this step has been taken
        """
        # Take a step in the random walk
        self._current_usage += int(
            self._variation * (random.random() - 0.5) * 2
        )

        # Enforce min/max clamps
        if self._clamp_min is not None:
            self._current_usage = max(self._current_usage, self._clamp_min)

        if self._clamp_max is not None:
            self._current_usage = min(self._current_usage, self._clamp_max)

        return self._current_usage

    def current_sample(self):
        """Return the current sample without taking a step"""
        return self._current_usage


def send_backhaul_usage_report(uplink_generator, downlink_generator):
    up_bytes = uplink_generator.take_step()
    down_bytes = downlink_generator.take_step()
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    backhaul_usage_payload = {
        'down_bytes': down_bytes,
        'up_bytes': up_bytes,
        'begin_timestamp': timestamp,
        'end_timestamp': timestamp,
    }

    marshalled_payload = cbor2.dumps(backhaul_usage_payload)

    headers = {"content-type": "application/cbor"}
    response = requests.post("http://localhost:8000/telemetry/backhaul",
                             headers=headers,
                             data=marshalled_payload,
                             )
    print("Backhaul POST:", response)


class ThreadedRepeater(threading.Thread):
    """Repeatedly calls the function at a given interval

    Note: The interval creeps forward by the function execution time and
    should not be used for precise timing.
    """
    def __init__(self, function, repeat_interval_s, run_first=False):
        super().__init__()
        self._stop_trigger = threading.Event()
        self._interval_s = repeat_interval_s
        self._function = function
        self._run_first = run_first

    def run(self):
        """Run method overriding Thread::run to call the function repeatedly
        """
        if self._run_first:
            self._function()
        while not self._stop_trigger.wait(self._interval_s):
            self._function()

    def stop(self):
        self._stop_trigger.set()


if __name__ == "__main__":
    uplink_usage_generator = UsageGenerator(
        baseline_usage=5 * (1000**2),
        max_step_variation=100 * (1000**1),
        clamp_min=0,
        clamp_max=15 * (1000**2),
    )

    downlink_usage_generator = UsageGenerator(
        baseline_usage=10 * (1000**2),
        max_step_variation=100 * (1000**1),
        clamp_min=0,
        clamp_max=15 * (1000**2),
    )

    backhaul_sender = ThreadedRepeater(
        lambda: send_backhaul_usage_report(
            uplink_usage_generator, downlink_usage_generator
        ),
        repeat_interval_s=10,
        run_first=True,
    )

    try:
        backhaul_sender.start()
    except KeyboardInterrupt:
        print("Shutting down threads-- ctrl+c again to hard exit")
        backhaul_sender.stop()
