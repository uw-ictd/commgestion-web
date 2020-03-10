from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Application(models.Model):
    host = models.CharField(max_length=255, unique=True)
    throughput = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return 'Application: {} -> {}'.format(self.host, self.throughput)


class UserDefinedHost(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'UserDefinedHost: {}'.format(self.name)


class HostMapping(models.Model):
    host = models.ForeignKey(UserDefinedHost, on_delete=models.CASCADE)
    captured_host = models.CharField(max_length=255)

    def __str__(self):
        return 'HostMapping: {} -> {}'.format(self.captured_host, self.host.name)


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


class Usage(models.Model):
    user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    throughput = models.FloatField()
    timestamp = models.DateTimeField()

    def get_username(self):
        return self.user.display_name

    def __str__(self):
        return 'Usage: {} -> {}'.format(self.timestamp, self.throughput)
