from django.test import TestCase
from django.utils import timezone

from web.models import Application


class ApplicationModelTest(TestCase):
    def test_application_creation(self):
        host_name = 'https://google.com/'
        Application.objects.create(
            host=host_name,
            throughput=1000,
            timestamp=timezone.now(),
        )

        created_application = Application.objects.get(host=host_name)
        self.assertEqual(created_application.host, host_name)
        self.assertEqual(created_application.throughput, 1000)
