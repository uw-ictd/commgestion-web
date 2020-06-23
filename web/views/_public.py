import json

from web.models import BackhaulUsage
from django.utils.translation import gettext_lazy as _


def generate_context():
    """Compute a django context dictionary for the public status view.
    """
    latest_backhaul_usage = BackhaulUsage.objects.latest("timestamp")
    print(latest_backhaul_usage)
    if latest_backhaul_usage is None:
        public_data = [0]
    else:
        public_data = [round(latest_backhaul_usage.total_kbytes/10, 2)]

    print(public_data)
    print(latest_backhaul_usage)

    return {
        "data": public_data,
        'title': json.dumps(str(_('Current network usage'))),
        'metric_title': json.dumps(str(_('Total Throughput'))),
    }
