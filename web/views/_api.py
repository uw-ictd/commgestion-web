import datetime
import json
from django import http

from web.models import (BackhaulUsage, RanUsage)


def datetime_string_converter(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)


def public_utilization(request):
    if request.method != "GET":
        return http.HttpResponseNotAllowed(['GET'], "Read only")

    response = {}

    latest_backhaul_usage = BackhaulUsage.objects.latest("timestamp")
    if latest_backhaul_usage is None:
        response["backhaul"] = {
            "up_bytes_per_second": 0,
            "down_bytes_per_second": 0,
        }
    else:
        # TODO(matt9j) Support variable intervals, be sure to handle zero case
        duration = 2.0
        up_bytes_per_second = latest_backhaul_usage.up_bytes / duration
        down_bytes_per_second = latest_backhaul_usage.down_bytes / duration
        response["backhaul"] = {
            "up_bytes_per_second": up_bytes_per_second,
            "down_bytes_per_second": down_bytes_per_second,
            "timestamp": latest_backhaul_usage.timestamp,
        }

    latest_ran_usage = RanUsage.objects.latest("timestamp")
    if latest_ran_usage is None:
        response["ran"] = {
            "up_bytes_per_second": 0,
            "down_bytes_per_second": 0,
        }
    else:
        # TODO(matt9j) Support variable intervals, be sure to handle zero case
        duration = 2.0
        up_bytes_per_second = latest_ran_usage.up_bytes / duration
        down_bytes_per_second = latest_ran_usage.down_bytes / duration
        response["ran"] = {
            "up_bytes_per_second": up_bytes_per_second,
            "down_bytes_per_second": down_bytes_per_second,
            "timestamp": latest_ran_usage.timestamp,
        }

    return http.HttpResponse(
        json.dumps(response, default=datetime_string_converter)
    )
