import json
import random
from web.models import Subscriber, Usage
from django.utils import timezone
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


def generate_test_data():
    GRAPH_TITLE = _('Current network usage').__str__()
    METRIC_TITLE = _('Total Throughput {}').__str__()
    DEFAULT_UNITS = _(' KBps').__str__()
    
    #make some "current usage" data (runs every time so we have fresh numbers)
    k = 5
    usr = Subscriber.objects.get(phonenumber='123456789' + str(random.randint(0, 4)))
    time = timezone.now()
    while k >= 0 :
        Usage.objects.create(user=usr, throughput=50*random.random(), timestamp=time)
        k-=1
    
    #query for the current usage
    qs_agg = Usage.objects.filter(timestamp__exact=time).aggregate(thru = Sum('throughput'))
    public_data =[round(qs_agg['thru'], 2)]
    # TODO: Do some computation here to find out if it's KBps or Mbps etc..,
    units_served = DEFAULT_UNITS

    return {
        "data": public_data,
        'title': json.dumps(GRAPH_TITLE),
        'metric_title': json.dumps(METRIC_TITLE.format(DEFAULT_UNITS)),
        'dimensions': json.dumps(units_served)
    }
