from web.models import Subscriber

def generate_table():
    all_subscribers = Subscriber.objects.all()
    return {"data": all_subscribers}