from datetime import (datetime, timezone)
from django.test import (TestCase, Client)
from http import HTTPStatus
from web import populate

import cbor2
import logging


class TrafficLoggerUserThroughputViewTest(TestCase):
    def setUp(self):
        # =============================
        # Disable logging for test runs
        logging.disable(logging.CRITICAL)
        # =============================
        self.c = Client(raise_request_exception=True)

    def test_non_post(self):
        response = self.c.get('/telemetry/user/')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(response['Allow'], 'POST')

    def test_bad_content_type(self):
        response = self.c.post('/telemetry/user/', data={'a':"fishsticks"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_bad_cbor(self):
        data = b'i-am-garbage-hear-me-r0ar'
        response = self.c.post('/telemetry/user/',
                               data=data,
                               content_type='application/cbor')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_missing_key(self):
        data = {'wrong_key': 'and_nothing_right'}
        marshalled_data = cbor2.dumps(data)
        response = self.c.post('/telemetry/user/',
                               data=marshalled_data,
                               content_type='application/cbor')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_subscriber_non_existence(self):
        data = {'user_id': '0',
                'throughput_kbps': 1234,
                'begin_timestamp': datetime.now(timezone.utc),
                'end_timestamp': datetime.now(timezone.utc),
                }

        marshalled_data = cbor2.dumps(data)
        response = self.c.post('/telemetry/user/',
                               data=marshalled_data,
                               content_type='application/cbor')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_end_to_end(self):
        # Use the populate module to generate known fake subscribers.
        populate.add_subscribers()

        data = {'user_id': '1234567890',
                'throughput_kbps': 1234,
                'begin_timestamp': datetime.now(timezone.utc),
                'end_timestamp': datetime.now(timezone.utc),
                }

        marshalled_data = cbor2.dumps(data)
        response = self.c.post('/telemetry/user/',
                               data=marshalled_data,
                               content_type='application/cbor')

        self.assertEqual(response.status_code, HTTPStatus.OK)
