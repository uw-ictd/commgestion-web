from web.models import Subscriber
from django.utils.translation import gettext_lazy as _


def generate_table():
    all_subscribers = Subscriber.objects.all()
    return {"data": all_subscribers}