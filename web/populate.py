import random

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from web.models import (HostUsage,
                        UserDefinedHost,
                        HostMapping,
                        Subscriber,
                        SubscriberUsage,
                        RanUsage,
                        BackhaulUsage,
                        )


def add_applications():
    """Add more applications
    """
    HostUsage.objects.all().delete()
    hosts = ['https://google.com/', 'https://facebook.com', 'https://whatsapp.com', 'https://santainesapp.mx']
    for host_name in hosts:
        HostUsage.objects.create(
            host=host_name,
            down_bytes=1000 * random.random(),
            up_bytes=50 * random.random(),
            timestamp=timezone.now(),
        )


def add_hostmappings():
    """Add host mapping as well as user defined hosts
    """
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


def add_subscribers(subscriber_total=10):
    """Add subscribers, which requires fake "User" info like email phone imsi
    """
    Subscriber.objects.all().delete()
    User.objects.filter(is_superuser=False).all().delete()

    SubscriberUsage.objects.all().delete()

    imsi_format = "91099{:010d}"
    email_format = "person{}@email.com"
    password_format = "password{}"

    for i in range(subscriber_total):
        imsi_value = imsi_format.format(i)
        email_value = email_format.format(i)
        password_value = password_format.format(i)

        User.objects.create_user(
            username=imsi_value,
            email=email_value,
            password=password_value
        )

        created_user = User.objects.get(username=imsi_value)

        Subscriber.objects.create(
            user=created_user,
            msisdn="713202{}".format(i),
            display_name=email_value.split('@')[0],
            imsi=imsi_value,
            is_local=True if i % 2 == 0 else False,
            role=Subscriber.Role.USER_ROLE,
            authorization_status=Subscriber.ConnectionStatus.AUTHORIZED,
            last_time_online=timezone.now(),
            rate_limit_kbps=100,
            equipment="equipment name {}".format(i),
            created=timezone.now(),
            subscription_date=timezone.now(),
            subscription_status=Subscriber.SubscriptionStatusKinds.PAID,
        )

        created_subscriber = Subscriber.objects.get(imsi=imsi_value)

        for j in range(30):
            SubscriberUsage.objects.create(
                subscriber=created_subscriber,
                down_bytes=50 * random.random(),
                up_bytes=10 * random.random(),
                timestamp=timezone.now() + timedelta(days=j),
            )


def add_fake_ran_usage(per_log_delta, total_span):
    """Add fake logs for overall radio access network (RAN) usage
    """
    # ToDo(matt9j) Separate create and destroy into separate functions
    RanUsage.objects.all().delete()

    # Generate the history going from this moment into the past
    base_time = timezone.now()
    end_time = base_time - total_span
    next_time_to_insert = base_time

    # Track the current throughput and vary as a random walk to draw a
    # continuous line.
    up_bytes = 5 * (1000**2)
    down_bytes = 10 * (1000**2)

    # Store objects in memory to bulk insert for efficiency
    usages_to_insert = list()

    while next_time_to_insert > end_time:
        usages_to_insert.append(RanUsage(
            timestamp=next_time_to_insert,
            up_bytes=up_bytes,
            down_bytes=down_bytes,
        ))

        next_time_to_insert -= per_log_delta
        up_bytes += int(100 * (1000**1) * (random.random() - 0.5))
        down_bytes += int(100 * (1000**1) * (random.random() - 0.5))
        down_bytes = max(down_bytes, 0)
        up_bytes = max(down_bytes, 0)

    RanUsage.objects.bulk_create(usages_to_insert)


def add_fake_backhaul_usage(per_log_delta, total_span):
    """Add fake logs for overall backhaul network usage
    """
    # ToDo(matt9j) Separate create and destroy into separate functions
    BackhaulUsage.objects.all().delete()

    # Generate the history going from this moment into the past
    base_time = timezone.now()
    end_time = base_time - total_span
    next_time_to_insert = base_time

    # Track the current throughput and vary as a random walk to draw a
    # continuous line.
    up_bytes = 5 * (1000**2)
    down_bytes = 10 * (1000**2)

    # Store objects in memory to bulk insert for efficiency
    usages_to_insert = list()

    while next_time_to_insert > end_time:
        usages_to_insert.append(BackhaulUsage(
            timestamp=next_time_to_insert,
            up_bytes=up_bytes,
            down_bytes=down_bytes,
        ))

        next_time_to_insert -= per_log_delta
        up_bytes += int(100 * (1000**1) * (random.random() - 0.5))
        down_bytes += int(100 * (1000**1) * (random.random() - 0.5))
        down_bytes = max(down_bytes, 0)
        up_bytes = max(down_bytes, 0)

    BackhaulUsage.objects.bulk_create(usages_to_insert)


def get_subscribers():
    total = Subscriber.objects.all()
    return total


def get_usage():
    return SubscriberUsage.objects.all()


def clear_and_add_defaults():
    add_subscribers(35)
    add_applications()
    add_hostmappings()
    # ToDo(matt9j) Ran usage not diplayed yet
    add_fake_ran_usage(timedelta(seconds=10), timedelta(days=30))
    # ToDo(matt9j) Figure out serverside resampling... keep a coarse time
    #  interval for now to display on the highcharts frontend
    add_fake_backhaul_usage(timedelta(minutes=60), timedelta(days=30))
