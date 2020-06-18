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
        public_data =[round(latest_backhaul_usage.total_kbytes/10, 2)]

    print(public_data)
    print(latest_backhaul_usage)

    # TODO: Do some computation here to find out if it's KBps or Mbps etc..,
    units_served = 'KBps'
    metric_title = "{} {}".format(str(_('Total Throughput')),
                                  str(_("KBps")),
                                  )

    return {
        "data": public_data,
        'title': json.dumps(str(_('Current network usage'))),
        'metric_title': json.dumps(metric_title),
        'dimensions': json.dumps(units_served)
    }
