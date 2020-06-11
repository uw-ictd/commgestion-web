from django.test import TestCase
from django.utils import timezone

from web.models import HostUsage


class ApplicationModelTest(TestCase):
    def test_application_creation(self):
        host_name = 'https://google.com/'
        HostUsage.objects.create(
            host=host_name,
            throughput=1000,
            timestamp=timezone.now(),
        )

        created_application = HostUsage.objects.get(host=host_name)
        self.assertEqual(created_application.host, host_name)
        self.assertEqual(created_application.total_kbytes, 1000)
