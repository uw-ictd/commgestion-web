import json

from django.db.models import Sum

from web.models import Subscriber, Usage

def lookup_user(user_id):
    subscriber = Subscriber.objects.get(pk=user_id)
    return subscriber.display_name


def generate_test_data():
    usageData = Usage.objects.values("user").annotate(Sum("throughput"))
    data = []
    for usage in usageData:
        data.append(
            {
                'name': lookup_user(usage['user']),
                'y': usage['throughput__sum'],
            }
        )
    return {'data': json.dumps(data)}