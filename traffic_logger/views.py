""" Views for the traffic_logger application

The traffic logger provides programatic APIs rather than rendered user-facing
pages. It uses CBOR for payload marshalling and unmarshalling.

 """
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseServerError, HttpResponseNotAllowed,
                         HttpResponseNotFound)

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from web.models import (HostUsage, Subscriber, SubscriberUsage)

import cbor2
import collections
import logging


# Setup the local error log
_error_log = logging.getLogger('commgestion.traffic_logger')


# TODO(matt9j) Ensure logging urls are only available on localhost.
@csrf_exempt
def log_user_throughput(request):
    request_payload, early_response = _parse_cbor_post_or_error(request)
    if early_response is not None:
        return early_response

    try:
        user_id = request_payload['user_id']
        # TODO(matt9j) Save a more informative throughput sketch (see NSDI paper)
        throughput = request_payload['throughput_kbps']
        begin_timestamp = request_payload['begin_timestamp']
        # TODO(matt9j) Support timestamp ranges
        end_timestamp = request_payload['end_timestamp']
    except KeyError as e:
        _error_log.warning("Rx user_log_throughput request with missing keys",
                           exc_info=True)
        return HttpResponseBadRequest(
            "Missing required request key {}".format(str(e)))

    # Lookup the appropriate matching subscriber.
    try:
        # TODO(matt9j) Can this be done with a single lookup?
        user_instance = User.objects.get(username=user_id)
        subscriber_instance = Subscriber.objects.get(user=user_instance)
    except ObjectDoesNotExist:
        _error_log.warning("user_id %s not found", user_id, exc_info=True)
        return HttpResponseNotFound(
            "requested user_id {} not found".format(user_id))

    # Create the usage object itself.
    try:
        SubscriberUsage.objects.create(user=subscriber_instance,
                                       throughput=throughput,
                                       timestamp=begin_timestamp)
    except (ObjectDoesNotExist, DatabaseError):
        _error_log.critical("Failed to write data", exc_info=True)
        return HttpResponseServerError("Internal server error")

    # The post was successful
    return HttpResponse("", status=200)


# TODO(matt9j) Ensure logging urls are only available on localhost.
@csrf_exempt
def log_host_throughput(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'],
                                      "Only POST is supported")

    request_payload, early_response = _parse_cbor_post_or_error(request)
    if early_response is not None:
        return early_response

    try:
        host_fqdn = request_payload['host_fqdn']
        # TODO(matt9j) Save a more informative throughput sketch (see NSDI paper)
        throughput = request_payload['throughput_kbps']
        begin_timestamp = request_payload['begin_timestamp']
        # TODO(matt9j) Support timestamp ranges
        end_timestamp = request_payload['end_timestamp']
    except KeyError as e:
        _error_log.warning("Rx host_log_throughput request with missing keys",
                           exc_info=True)
        return HttpResponseBadRequest(
            "Missing required request key {}".format(str(e)))

    # Create the host usage object itself.
    try:
        HostUsage.objects.create(host=host_fqdn,
                                 throughput=throughput,
                                 timestamp=begin_timestamp)
    except (ObjectDoesNotExist, DatabaseError):
        _error_log.critical("Failed to write data", exc_info=True)
        return HttpResponseServerError("Internal server error")

    # The post was successful
    return HttpResponse("", status=200)


def _parse_cbor_post_or_error(request):
    """Validate the request is actually the expected CBOR post

    Returns the valid parsed payload or an appropriate http error response
    for the error that occurred.
    """
    request_payload = None
    response = None
    if request.method != "POST":
        response = HttpResponseNotAllowed(['POST'],
                                          "Only POST is supported")
        return request_payload, response

    if request.content_type != "application/cbor":
        response = HttpResponseBadRequest(
            'Content type must be cbor "application/cbor"')
        return request_payload, response
    try:
        request_payload = cbor2.loads(request.body)
    except cbor2.CBORDecodeError as e:
        _error_log.warning("Rx malformed log_host_throughput request",
                           exc_info=e, stack_info=True)
        response = HttpResponseBadRequest("Unable to parse request body as CBOR")
        return request_payload, response

    if not isinstance(request_payload, collections.Mapping):
        # CBOR will generously parse most strings without error, ensure the
        # payload is a key:value mapping as expected.
        _error_log.warning("Malformed cbor payload received", exc_info=True)
        response = HttpResponseBadRequest("Request payload malformed")
        return request_payload, response

    return request_payload, response
