from web.models import Subscriber
from django.core import serializers

def generate_table():
    all_subscribers = Subscriber.objects.all()
    return {"data": all_subscribers}