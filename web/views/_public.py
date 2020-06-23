import json

from django.utils.translation import gettext_lazy as _


def generate_context():
    """Compute a django context dictionary for the public status view.
    """

    return {
        'title': json.dumps(str(_('Current network usage'))),
        'metric_title': json.dumps(str(_('Total Throughput'))),
    }
