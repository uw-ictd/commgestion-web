from django.test import TestCase
from web.models import UserDefinedHost


class UserDefinedHostModelTests(TestCase):
    def test_check_host_names(self):
        """
        Check if the UserDefinedHosts are correctly inserted into the database.
        """
        # Create the objects
        UserDefinedHost.objects.create(name="facebook.com")
        UserDefinedHost.objects.create(name="google.com")

        # Query the objects as required.
        fb_host = UserDefinedHost.objects.get(name="facebook.com")
        google_host = UserDefinedHost.objects.get(name="google.com")
        self.assertEqual(fb_host.name, "facebook.com", "Facebook host name is correct")
        self.assertEqual(google_host.name, "google.com", "Google host name is correct")
        all_hosts = UserDefinedHost.objects.all()
        self.assertEqual(
            len(all_hosts), 2, "2 values were correctly retrieved from the database"
        )
        host_count = UserDefinedHost.objects.count()
        self.assertEqual(host_count, 2, "Count using the django ORM provided count()")
