from django.contrib.auth.models import User
from django.test import TestCase
from web.models import Subscriber, SubscriberUsage

from django.utils import timezone

IMSI_VALUE = "1234567890"
EMAIL_VALUE = "person@ccellular.network"
PASSWORD = "changethisP@ssw0rd"
GUTI_VALUE = "ThisIsAGutiValue"


class SubscriberModelTest(TestCase):
    def test_subscriber_creation(self):
        # insert user into database
        User.objects.create_user(
            username=IMSI_VALUE, email=EMAIL_VALUE, password=PASSWORD
        )

        created_user = User.objects.get(username=IMSI_VALUE)

        INSERT_TIMESTAMP = timezone.now()

        Subscriber.objects.create(
            user=created_user,
            phonenumber=IMSI_VALUE,
            display_name=EMAIL_VALUE.split("@")[0],
            imsi=IMSI_VALUE,
            guti=GUTI_VALUE,
            is_local=True,
            role=Subscriber.Role.USER_ROLE,
            connectivity_status=Subscriber.ConnectionStatus.ONLINE,
            last_time_online=INSERT_TIMESTAMP,
            rate_limit_kbps=100,
        )

        created_subscriber = Subscriber.objects.get(phonenumber=IMSI_VALUE)

        # Validating the Subscriber information.
        self.assertEqual(created_subscriber.user, created_user)
        self.assertEqual(created_subscriber.msisdn, IMSI_VALUE)
        self.assertEqual(created_subscriber.display_name, "person")
        self.assertEqual(created_subscriber.imsi, IMSI_VALUE)
        self.assertEqual(created_subscriber.guti, GUTI_VALUE)
        self.assertTrue(created_subscriber.is_local)
        self.assertEqual(created_subscriber.role, Subscriber.Role.USER_ROLE)
        self.assertEqual(
            created_subscriber.authorization_status, Subscriber.ConnectionStatus.ONLINE
        )
        self.assertEqual(created_subscriber.last_time_online, INSERT_TIMESTAMP)
        self.assertEqual(created_subscriber.rate_limit_kbps, 100)

        # Validating the User information
        self.assertEqual(created_user.get_username(), IMSI_VALUE)
        self.assertTrue(created_user.check_password(PASSWORD))
        self.assertEqual(created_user.email, EMAIL_VALUE)

        s_value = str(created_subscriber)
        self.assertEqual(s_value, "Subscriber: {}".format(IMSI_VALUE))

        # Start testing for SubscriberUsage
        SubscriberUsage.objects.create(
            subscriber=created_subscriber,
            up_bytes=10,
            down_bytes=10,
            timestamp=timezone.now(),
        )

        SubscriberUsage.objects.create(
            subscriber=created_subscriber,
            up_bytes=15,
            down_bytes=15,
            timestamp=timezone.now(),
        )

        # Query usage per subscriber using foreignKey filter
        usage_list = SubscriberUsage.objects.filter(subscriber=created_subscriber)
        self.assertEqual(len(usage_list), 2)

        # Query for usage using subscriber object
        usage_list_from_subscriber = created_subscriber.subscriberusage_set.all()
        self.assertEqual(len(usage_list_from_subscriber), 2)

        self.assertEqual(len(usage_list), len(usage_list_from_subscriber))
        for i in range(0, len(usage_list)):
            usage_1 = usage_list[i]
            usage_2 = usage_list_from_subscriber[i]
            self.assertEqual(usage_1, usage_2)
