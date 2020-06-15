from datetime import (datetime, timezone)
from django.test import (TestCase, Client)
from http import HTTPStatus
from web import populate
from tests.cbor_base_tests import CborBaseTests

import cbor2
import logging


class TelemetryRanUsageViewTest(CborBaseTests.ApiTest):
    def setUp(self):
        # =============================
        # Disable logging for test runs
        logging.disable(logging.CRITICAL)
        # =============================
        self.c = Client(raise_request_exception=True)
        super().set_parameters(self.c, '/telemetry/ran/')

    def test_non_post(self):
        response = self.c.get('/telemetry/ran/')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(response['Allow'], 'POST')

    def test_end_to_end(self):
        # Use the populate module to generate known fake subscribers.
        populate.add_subscribers()

        data = {'up_bytes': 1234,
                'down_bytes': 4321,
                'begin_timestamp': datetime.now(timezone.utc),
                'end_timestamp': datetime.now(timezone.utc),
                }

        marshalled_data = cbor2.dumps(data)
        response = self.c.post('/telemetry/ran/',
                               data=marshalled_data,
                               content_type='application/cbor')

        self.assertEqual(response.status_code, HTTPStatus.OK)
