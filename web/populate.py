from django.contrib.auth.models import User
from web.models import Application, UserDefinedHost, HostMapping, Subscriber, Usage
from collections import namedtuple
import random
from django.utils import timezone

#from django.contrib.auth.models import User

# add more applications
def add_applications():
    hosts = ['https://google.com/', 'https://facebook.com', 'https://whatsapp.com', 'https://santainesapp.mx']
    for host_name in hosts:
        Application.objects.create(
            host=host_name,
            throughput=1000 * random.random(),
            timestamp=timezone.now())

#  add host mapping as well as user defined hosts
def add_hostmappings():
    UserDefinedHost.objects.all().delete()
    captured_fb = list(['fb.cdn.com', 'dragon.cdn.com'])
    captured_google = list(['google.com','googlehost1.com', 'googlehost2.com', 'googlehost3'])
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
        
    udh_list = [(udh_fb, captured_fb),  (udh_google, captured_google),
    (udh_youtube, captured_youtube), (udh_wiki, captured_wikipedia)]

    for hm in udh_list:
        HostMapping.objects.create(host=hm[0], captured_host=hm[1])

    print(UserDefinedHost.objects.all())
""" 
#add subscribers, which requires fake "User" info like email phone imsi
def add_subscribers():
 """
def add_subscribers():
    Subscriber.objects.all().delete()
    User.objects.all().delete()
    Usage.objects.all().delete()

    IMSI_VALUES = ['1234567890', '1234567891','1234567892','1234567893','1234567894', '423456378', '234532']
    EMAIL_VALUES = ['person@ccellular.network','person1@ccellular.network','person2@ccellular.network',
    'person3@ccellular.network','person4@ccellular.network', 'hello@gmail.com', 'person@yahoo.com']
    PASSWORDS = ['changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd',
                 'password1', 'password2']
    GUTI_VALUES = ['GutiValue1','GutiValue2','GutiValue3','GutiValue4','GutiValue5', 'GutiValue6', 'GutiValue7']
    created_users = []
    #make users
    for i in range(len(IMSI_VALUES)):
        User.objects.create_user(username=IMSI_VALUES[i], email = EMAIL_VALUES[i], password=PASSWORDS[i])
        created_user = User.objects.get(username=IMSI_VALUES[i])
        created_users.append(created_user)
        INSERT_TIMESTAMP = timezone.now()
    
    #make subscribers
    for i in range(len(created_users)):
        user = created_users[i]
        Subscriber.objects.create(
            user=user,
            phonenumber=IMSI_VALUES[i],
            display_name=EMAIL_VALUES[i].split('@')[0],
            imsi=IMSI_VALUES[i],
            guti=GUTI_VALUES[i],
            is_local=True,
            role=Subscriber.Role.USER_ROLE,
            connectivity_status=Subscriber.ConnectionStatus.ONLINE,
            last_time_online=INSERT_TIMESTAMP,
            rate_limit_kbps=100,
        )
        
    subs = Subscriber.objects.all()
  
    for sub in subs:
        k = 5
        usr = Subscriber.objects.get(phonenumber=IMSI_VALUES[i])
        time = timezone.now()
        while k >= 0 :
            Usage.objects.create(user=usr, throughput=50*random.random(), timestamp=time)
            k-=1

def get_subscribers():
    total = Subscriber.objects.all()
    return total
def get_usage():
    return Usage.objects.all()