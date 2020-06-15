import json

from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from web.models import Subscriber, SubscriberUsage
from django.utils.formats import date_format


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
    NO_DATA_ERROR_MESSAGE = _("No Data available between the chosen dates.<br>Please search for a different time.").__str__()

    if from_date and to_date:
        from_date_string = from_date.strftime('%d %b %Y')
        to_date_string = to_date.strftime('%d %b %Y')
        title_with_date = GRAPH_TITLE + " between " + from_date_string + " and " + to_date_string
        usageData = SubscriberUsage.objects.filter(timestamp__range=[from_date, to_date])\
                        .values('subscriber')\
                        .annotate(total_bytes=(Sum("down_bytes") + Sum("up_bytes")))\
                        .order_by('-total_bytes') #sums the current row
    else:
        title_with_date = GRAPH_TITLE
        usageData = SubscriberUsage.objects.values("subscriber")\
                        .annotate(total_bytes=(Sum("down_bytes") + Sum("up_bytes")))\
                        .order_by('-total_bytes') #sums the current row

    total_consumed = sum([usage['total_bytes'] for usage in usageData]) #calculates sum of the total table
    data = []
    percent_consumed = 0.0
    left_over_sum = 0
    drilldown_data = []

    for usage in usageData:
        if percent_consumed <= MAX_PERCENT_TO_START_MERGE:
            percent_consumed += float(usage['total_bytes']) / total_consumed
            data.append(
                {
                    'name': lookup_user(usage['subscriber']),
                    'y': usage['total_bytes']
                }
            )
        else:
            drilldown_data.append([lookup_user(usage['subscriber']), usage['total_bytes']])
            left_over_sum += usage['total_bytes']
    if left_over_sum > 0:
        data.append({
            'name': _('Other (Merged)').__str__(),
            'y': left_over_sum,
            'drilldown': "Other (Merged)"
        })
    drilldown_response = build_drilldown_information('Other (Merged)', drilldown_data)

    return {
        'data': json.dumps(data),
        'drilldown': json.dumps(drilldown_response),
        'title': json.dumps(title_with_date),
        'errorMessage': json.dumps(NO_DATA_ERROR_MESSAGE),
    }
