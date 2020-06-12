from random import randint

from django.contrib.auth.models import User
from django.db import models


class SubscriberManager(models.Manager):
    def random(self):
        count = self.aggregate(count=models.Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Subscriber(models.Model):

    class Role:
        ADMIN_ROLE = 1
        USER_ROLE = 2
        RESEARCHER_ROLE = 3

    class ConnectionStatus:
        ONLINE = 1
        OFFLINE = 2
        BLOCKED = 3

    ROLE_CHOICES = (
        (Role.ADMIN_ROLE, u'admin'),
        (Role.USER_ROLE, u'user'),
        (Role.RESEARCHER_ROLE, u'researcher'),
    )

    CONN_CHOICES = (
        (ConnectionStatus.ONLINE, u'online'),
        (ConnectionStatus.OFFLINE, u'offline'),
        (ConnectionStatus.BLOCKED, u'blocked'),
    )

    objects = SubscriberManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    imsi = models.CharField(max_length=50)
    guti = models.CharField(max_length=50)
    is_local = models.BooleanField()
    role = models.IntegerField(choices=ROLE_CHOICES)  # TODO: Check if this can be replaced from auth.groups in User
    connectivity_status = models.IntegerField(choices=CONN_CHOICES)
    last_time_online = models.DateTimeField()
    rate_limit_kbps = models.IntegerField()

    def __str__(self):
        return "Subscriber: {}".format(self.imsi)


class RanUsage(models.Model):
    timestamp = models.DateTimeField()

    up_bytes = models.BigIntegerField()
    down_bytes = models.BigIntegerField()

    @property
    def total_kbytes(self):
        return float(self.up_bytes + self.down_bytes)/1000

    def __str__(self):
        return 'RanUsage: {} -> {}'.format(self.timestamp, self.total_kbytes)


class BackhaulUsage(models.Model):
    timestamp = models.DateTimeField()

    up_bytes = models.BigIntegerField()
    down_bytes = models.BigIntegerField()

    @property
    def total_kbytes(self):
        return float(self.up_bytes + self.down_bytes)/1000

    def __str__(self):
        return 'BackhaulUsage: {} -> {}'.format(self.timestamp, self.total_kbytes)


class SubscriberUsage(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    up_bytes = models.BigIntegerField()
    down_bytes = models.BigIntegerField()

    @property
    def total_kbytes(self):
        return float(self.up_bytes + self.down_bytes)/1000

    def get_username(self):
        return self.subscriber.display_name

    def __str__(self):
        return 'SubscriberUsage: {} -> {}'.format(self.timestamp, self.total_kbytes)


class HostUsage(models.Model):
    host = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField()

    up_bytes = models.BigIntegerField()
    down_bytes = models.BigIntegerField()

    @property
    def total_kbytes(self):
        return float(self.up_bytes + self.down_bytes)/1000

    def __str__(self):
        return 'HostUsage: {} -> {}'.format(self.host, self.total_kbytes)


class UserDefinedHost(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'UserDefinedHost: {}'.format(self.name)


class HostMapping(models.Model):
    host = models.ForeignKey(UserDefinedHost, on_delete=models.CASCADE)
    captured_host = models.CharField(max_length=255)

    def __str__(self):
        return 'HostMapping: {} -> {}'.format(self.captured_host, self.host.name)
