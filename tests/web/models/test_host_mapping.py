from django.test import TestCase
from web.models import HostMapping, UserDefinedHost


class HostMappingModelTest(TestCase):
    def test_host_mapping_creation(self):
        captured_host_list = list(["fb.cdn.com", "dragon.cdn.com"])

        UserDefinedHost.objects.create(name="facebook.com")
        udh = UserDefinedHost.objects.get(name="facebook.com")
        HostMapping.objects.create(host=udh, captured_host=captured_host_list[0])
        HostMapping.objects.create(host=udh, captured_host=captured_host_list[1])

        # Now retrieve the information for a given user
        mapped_hosts_of_facebook = udh.hostmapping_set.all()
        self.assertEqual(len(mapped_hosts_of_facebook), 2)
        self.assertEqual(
            mapped_hosts_of_facebook[0].captured_host, captured_host_list[0]
        )
        self.assertEqual(
            mapped_hosts_of_facebook[1].captured_host, captured_host_list[1]
        )
