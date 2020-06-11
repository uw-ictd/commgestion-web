from datetime import timedelta

from django.contrib.auth.models import User
from web.models import HostUsage, UserDefinedHost, HostMapping, Subscriber, SubscriberUsage
import random
from django.utils import timezone
from datetime import date
from datetime import time
from datetime import datetime


# from django.contrib.auth.models import User

# add more applications
def add_applications():
    HostUsage.objects.all().delete()
    hosts = ['https://google.com/', 'https://facebook.com', 'https://whatsapp.com', 'https://santainesapp.mx']
    for host_name in hosts:
        HostUsage.objects.create(
            host=host_name,
            down_kbytes=1000 * random.random(),
            up_kbytes=50 * random.random(),
            timestamp=timezone.now(),
        )


#  add host mapping as well as user defined hosts
def add_hostmappings():
    UserDefinedHost.objects.all().delete()
    captured_fb = list(['fb.cdn.com', 'dragon.cdn.com'])
    captured_google = list(['google.com', 'googlehost1.com', 'googlehost2.com', 'googlehost3'])
    captured_youtube = list(['youtube.com', 'you1', 'youhost2'])
    captured_wikipedia = list(['wikipedia.org', 'wiki', 'wik', 'wik2'])

    UserDefinedHost.objects.create(name='google.com')
    udh_google = UserDefinedHost.objects.get(name='google.com')
    UserDefinedHost.objects.create(name='facebook.com')
    udh_fb = UserDefinedHost.objects.get(name='facebook.com')
    UserDefinedHost.objects.create(name='youtube.com')
    udh_youtube = UserDefinedHost.objects.get(name='youtube.com')
    UserDefinedHost.objects.create(name='wikipedia.org')
    udh_wiki = UserDefinedHost.objects.get(name='wikipedia.org')

    udh_list = [(udh_fb, captured_fb), (udh_google, captured_google),
                (udh_youtube, captured_youtube), (udh_wiki, captured_wikipedia)]

    for hm in udh_list:
        for captured_fqdn in hm[1]:
            HostMapping.objects.create(host=hm[0], captured_host=captured_fqdn)

    print(UserDefinedHost.objects.all())


def add_subscribers(subscriber_total=10):
    """
    #add subscribers, which requires fake "User" info like email phone imsi
    def add_subscribers():
    """
    Subscriber.objects.all().delete()
    User.objects.filter(is_superuser=False).all().delete()

    SubscriberUsage.objects.all().delete()

    imsi_format = "123456789{}"
    email_format = "person{}@email.com"
    password_format = "password{}"
    guti_format = "guti_value{}"

    for i in range(subscriber_total):
        imsi_value = imsi_format.format(i)
        email_value = email_format.format(i)
        password_value = password_format.format(i)
        guti_value = guti_format.format(i)
        User.objects.create_user(username=imsi_value, email=email_value, password=password_value)
        created_user = User.objects.get(username=imsi_value)
        INSERT_TIMESTAMP = timezone.now()

        Subscriber.objects.create(
            user=created_user,
            phonenumber=imsi_value,
            display_name=email_value.split('@')[0],
            imsi=imsi_value,
            guti=guti_value,
            is_local=True if i % 2 == 0 else False,
            role=Subscriber.Role.USER_ROLE,
            connectivity_status=Subscriber.ConnectionStatus.ONLINE,
            last_time_online=INSERT_TIMESTAMP,
            rate_limit_kbps=100,
        )

        created_subscriber = Subscriber.objects.get(phonenumber=imsi_value)
        # for j in range(30):
        #     SubscriberUsage.objects.create(user=created_subscriber, throughput=50 * random.random(), timestamp=timezone.now())

        #print( datetime.now() + timedelta(days=1))
        #Subtract 60 seconds.
        #print( datetime.now() - timedelta(seconds=60))
        #Add 2 years.
        #print( datetime.now() + timedelta(days=730))

        for j in range(30):
            SubscriberUsage.objects.create(
                subscriber=created_subscriber,
                down_kbytes=50 * random.random(),
                up_kbytes=10 * random.random(),
                timestamp=timezone.now(),
            )
            #having trouble printing anything out
            #where is the bug
            print(datetime.now() + timedelta(days=1))
            print(datetime.now() + timedelta(weeks=1))

def get_subscribers():
    total = Subscriber.objects.all()
    return total


def get_usage():
    return SubscriberUsage.objects.all()


add_subscribers(35)
add_applications()
add_hostmappings()
