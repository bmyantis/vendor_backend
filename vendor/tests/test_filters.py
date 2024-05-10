from model_bakery import baker

from django.test import TestCase
from django_filters import CharFilter
from django.contrib.auth import get_user_model

from vendor.filters import VendorFilter
from vendor.models import Vendor

User = get_user_model()


class VendorFilterTestCase(TestCase):
    def test_filter_fields(self):
        # Create a test vendor
        self.vendor1 = baker.make(Vendor, name='Vendor 1')
        self.vendor2 = baker.make(Vendor, name='Vendor 2')
        
        # Initialize the filter with data
        filter_data = {'name': self.vendor1.name}
        filter_set = VendorFilter(data=filter_data, queryset=Vendor.objects.all())

        # Check if filter set is valid
        self.assertTrue(filter_set.is_valid())

        # Check if expected filters are present
        self.assertIsInstance(filter_set.filters['name'], CharFilter)

        # Check if filtering works as expected
        filtered_queryset = filter_set.qs
        self.assertEqual(filtered_queryset.count(), 1)
