#! /usr/bin/env python
import cbor2
import datetime
import requests


if __name__ =="__main__":
    payload = {
    'user_id': "12345678901",
    'throughput_kbps': 1234,
    'begin_timestamp': datetime.datetime.now(datetime.timezone.utc),
    'end_timestamp': datetime.datetime.now(datetime.timezone.utc),
    }

    marshalled_payload = cbor2.dumps(payload)

    response = requests.post("http://localhost:8000/traffic-logger/user", data=marshalled_payload)

    print(response)
    print(response.content)

    exit(0)
