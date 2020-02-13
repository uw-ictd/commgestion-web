from web.models import Subscriber
from django.core import serializers

def generate_table():
    all_subscribers = Subscriber.objects.all()
    json = serializers.serialize('json', all_subscribers)
    return {"data": json}