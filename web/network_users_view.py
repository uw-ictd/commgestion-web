import json

from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from web.models import Subscriber, Usage


def lookup_user(user_id):
    subscriber = Subscriber.objects.get(pk=user_id)
    return subscriber.display_name


def build_drilldown_information(drilldown_name, drilldown_data):
    return {
        'name': drilldown_name,
        'id': drilldown_name,
        'data': drilldown_data
    }


def generate_test_data(from_date=None, to_date=None):
    MAX_PERCENT_TO_START_MERGE = 0.75  # TODO: Do this by the number of users if necessary i.e. limit to 10 users etc..,
    GRAPH_TITLE = _('Use of community data').__str__()

    if from_date and to_date:
        usageData = Usage.objects.filter(timestamp__range=[from_date, to_date])\
                        .values('user')\
                        .annotate(Sum("throughput"))\
                        .order_by('-throughput__sum') #sums the current row
    else:
        usageData = Usage.objects.values("user")\
                        .annotate(Sum("throughput"))\
                        .order_by('-throughput__sum') #sums the current row

    total_consumed = sum([usage['throughput__sum'] for usage in usageData]) #calculates sum of the total table
    data = []
    percent_consumed = 0.0
    left_over_sum = 0
    drilldown_data = []
    for usage in usageData:
        if percent_consumed <= MAX_PERCENT_TO_START_MERGE:
            percent_consumed += float(usage['throughput__sum']) / total_consumed
            data.append(
                {
                    'name': lookup_user(usage['user']),
                    'y': usage['throughput__sum']
                }
            )
        else:
            drilldown_data.append([lookup_user(usage['user']), usage['throughput__sum']])
            left_over_sum += usage['throughput__sum']
    if left_over_sum > 0:
        data.append({
            'name': _('Other (Merged)').__str__(),
            'y': left_over_sum,
            'drilldown': "Other (Merged)"
        })
    drilldown_response = build_drilldown_information('Other (Merged)', drilldown_data)
    title_with_date = GRAPH_TITLE + " " + from_date.__str__() + " - " + to_date.__str__()
    return {
        'data': json.dumps(data),
        'drilldown': json.dumps(drilldown_response),
        'title': json.dumps(title_with_date)
    }
