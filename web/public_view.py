import json
import random
from datetime import timedelta, datetime

from web.models import Subscriber, Usage
from django.utils import timezone
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


def generate_test_data():
    GRAPH_TITLE = _('Current network usage').__str__()
    METRIC_TITLE = _('Total Throughput {}').__str__()
    DEFAULT_UNITS = _(' KBps').__str__()

    HOURS = 24
    TIME_THRESHOLD = timedelta(hours=HOURS)  # TODO: Replace with days= if necessary
    SECONDS = HOURS * 60 * 60
    
    #make some "current usage" data (runs every time so we have fresh numbers)
    try:
        k = 5
        random_subscriber = Subscriber.objects.random()  # Fetch a random subscriber.
        # usr = Subscriber.objects.get(phonenumber='123456789' + str(random.randint(0, 4)))
        current_time = timezone.now()
        time_least_bound = current_time - TIME_THRESHOLD

        # TODO: Fix this test script as necessary and avoid writing data into the database this way.
        while k >= 0 :
            Usage.objects.create(user=random_subscriber, throughput=5000*random.random(), timestamp=current_time)
            k-=1

        # query for the current usage over the last 1 day.
        qs_agg = Usage.objects.filter(timestamp__gt=time_least_bound).aggregate(thru=Sum('throughput'))
        if 'thru' not in qs_agg or qs_agg['thru'] is None:
            public_data = [0]
        else:
            public_data =[round(qs_agg['thru']/SECONDS, 2)]
    except Exception as e:
        public_data = []
    # TODO: Do some computation here to find out if it's KBps or Mbps etc..,
    units_served = DEFAULT_UNITS

    return {
        "data": public_data,
        'title': json.dumps(GRAPH_TITLE),
        'metric_title': json.dumps(METRIC_TITLE.format(DEFAULT_UNITS)),
        'dimensions': json.dumps(units_served)
    }
