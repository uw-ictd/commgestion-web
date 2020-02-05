import json
import random
from web.models import Subscriber, Usage
from django.utils import timezone
from django.db.models import Sum

def generate_test_data():
    
    #make some "current usage" data (need this to run every time so that we can have some fresh numbers. 
    k = 5
    usr = Subscriber.objects.get(phonenumber='123456789' + str(random.randint(0, 5)))
    time = timezone.now()
    while k >= 0 :
        Usage.objects.create(user=usr, throughput=50*random.random(), timestamp=time)
        k-=1
    
    #query for the current usage:
    qs_agg = Usage.objects.filter(timestamp=time).annotate(thru = Sum('throughput'))
    print(qs_agg)
    data =[4]
    return {"data": data}