from django.test import TestCase
from vendor.models import Vendor, HistoricalPerformance


class VendorModelTest(TestCase):
    def test_vendor_code_generation(self):
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")
        self.assertIsNotNone(vendor.code)
        self.assertEqual(len(vendor.code), 12)

    def test_vendor_str_representation(self):
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")
        self.assertEqual(str(vendor), "Test Vendor")


class HistoricalPerformanceModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")

    def test_historical_performance_str_representation(self):
        historical_performance = HistoricalPerformance.objects.create(vendor=self.vendor)
        self.assertEqual(str(historical_performance), "Test Vendor")
