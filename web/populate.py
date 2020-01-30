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
    IMSI_VALUES = ['1234567890', '1234567891','1234567892','1234567893','1234567894']
    EMAIL_VALUES = ['person@ccellular.network','person1@ccellular.network','person2@ccellular.network',
    'person3@ccellular.network','person4@ccellular.network']
    PASSWORDS = ['changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd','changethisP@ssw0rd']
    GUTI_VALUES = ['GutiValue1','GutiValue2','GutiValue3','GutiValue4','GutiValue5']
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
        
        #add some usage for this subscriber
        created_subscriber = Subscriber.objects.get(phonenumber=IMSI_VALUES[i])
        Usage.objects.create(user=created_subscriber, throughput=50*random.random(), timestamp=timezone.now())

def get_subscribers():
    total = Subscriber.objects.all()
    return total

""" class SubscriberModelTest(TestCase):
    def test_subscriber_creation(self):
        #insert user into database
        User.objects.create_user(username=IMSI_VALUE, email=EMAIL_VALUE, password=PASSWORD)

        created_user = User.objects.get(username=IMSI_VALUE)

        INSERT_TIMESTAMP = timezone.now()

        Subscriber.objects.create(
            user=created_user,
            phonenumber=IMSI_VALUE,
            display_name=EMAIL_VALUE.split('@')[0],
            imsi=IMSI_VALUE,
            guti=GUTI_VALUE,
            is_local=True,
            role=Subscriber.Role.USER_ROLE,
            connectivity_status=Subscriber.ConnectionStatus.ONLINE,
            last_time_online=INSERT_TIMESTAMP,
            rate_limit_kbps=100,
        )

        created_subscriber = Subscriber.objects.get(phonenumber=IMSI_VALUE)




        # Start testing for Usage
        Usage.objects.create(user=created_subscriber, throughput=10, timestamp=timezone.now())
        Usage.objects.create(user=created_subscriber, throughput=15, timestamp=timezone.now())

        # Query usage per subscriber using foreignKey filter
        usage_list = Usage.objects.filter(user=created_subscriber)
        self.assertEqual(len(usage_list), 2)

        # Query for usage using subscriber object
        usage_list_from_subscriber = created_subscriber.usage_set.all()
        self.assertEqual(len(usage_list_from_subscriber), 2)

        self.assertEqual(len(usage_list), len(usage_list_from_subscriber))
        for i in range(0, len(usage_list)):
            usage_1 = usage_list[i]
            usage_2 = usage_list_from_subscriber[i]
            self.assertEqual(usage_1, usage_2)
 """