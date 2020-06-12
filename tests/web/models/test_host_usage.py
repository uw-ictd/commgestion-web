from django.test import TestCase
from django.utils import timezone

from web.models import HostUsage


class HostUsageModelTest(TestCase):
    def test_host_usage_creation(self):
        host_name = 'https://google.com/'
        HostUsage.objects.create(
            host=host_name,
            up_bytes=1000,
            down_bytes=1000,
            timestamp=timezone.now(),
        )

        created = HostUsage.objects.get(host=host_name)
        self.assertEqual(created.host, host_name)

        self.assertEqual(created.up_bytes, 1000)
        self.assertEqual(created.down_bytes, 1000)
