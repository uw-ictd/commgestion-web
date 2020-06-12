from django.test import (TestCase, Client)
from http import HTTPStatus

import cbor2


class CborBaseTests:
    # This blank parent class (no object parent) prevents the children from
    # being discovered by the unittest runner and run directly.
    class ApiTest(TestCase):
        def set_parameters(self, client, url):
            self.c = client
            self.url = url

        def test_bad_content_type(self):
            response = self.c.post(self.url, data={'a':"fishsticks"})
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        def test_bad_cbor(self):
            data = b'i-am-garbage-hear-me-r0ar'
            response = self.c.post(self.url,
                                   data=data,
                                   content_type='application/cbor')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        def test_missing_key(self):
            data = {'wrong_key_1337_42': 'and_nothing_right'}
            marshalled_data = cbor2.dumps(data)
            response = self.c.post(self.url,
                                   data=marshalled_data,
                                   content_type='application/cbor')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
