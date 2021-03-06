from django.test import TestCase
from django.utils import timezone

from web.models import RanUsage


class HostUsageModelTest(TestCase):
    def test_host_usage_creation(self):
        timestamp = timezone.now()
        RanUsage.objects.create(
            up_bytes=1000,
            down_bytes=1000,
            timestamp=timestamp,
        )

        created = RanUsage.objects.get(timestamp=timestamp)
        self.assertEqual(created.timestamp, timestamp)

        self.assertEqual(created.up_bytes, 1000)
        self.assertEqual(created.down_bytes, 1000)
