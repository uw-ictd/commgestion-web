from django.test import TestCase
from django.utils import timezone

from web.models import BackhaulUsage


class BackhaulUsageModelTest(TestCase):
    def test_backhaul_usage_creation(self):
        timestamp = timezone.now()
        BackhaulUsage.objects.create(
            up_bytes=1000,
            down_bytes=1000,
            timestamp=timestamp,
        )

        created = BackhaulUsage.objects.get(timestamp=timestamp)
        self.assertEqual(created.timestamp, timestamp)

        self.assertEqual(created.up_bytes, 1000)
        self.assertEqual(created.down_bytes, 1000)
