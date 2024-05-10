from django.test import TestCase
from vendor.serializers import VendorDeserializer, VendorSerializer, HistoricalPerformanceSerializer
from vendor.models import Vendor, HistoricalPerformance


class VendorDeserializerTest(TestCase):
    def test_valid_vendor_serializer(self):
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
        }
        serializer = VendorDeserializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.name, data['name'])
        self.assertEqual(instance.contact_details, data['contact_details'])
        self.assertEqual(instance.address, data['address'])

    def test_invalid_vendor_serializer(self):
        # Test for missing name
        data = {
            'contact_details': 'New Contact',
            'address': 'New Address',
        }
        serializer = VendorDeserializer(data=data)
        self.assertFalse(serializer.is_valid())


class VendorSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", code="vendor_code")
        
    def test_vendor_serializer(self):
        expected = {
            'id': str(self.vendor.id),
            'name': self.vendor.name,
            'code': self.vendor.code,
            'contact_details': self.vendor.contact_details,
            'address': self.vendor.address,
        }
        actual = VendorSerializer(instance=self.vendor).data
        self.assertDictEqual(expected, actual)


class HistoricalPerformanceSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", code="vendor_code")
        self.historical_performance = HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=0.95, quality_rating_avg=4.5, average_response_time=24, fulfillment_rate=0.98)

    def test_valid_historical_performance_serializer(self):
        expected = {
            'id': str(self.historical_performance.id),
            'vendor': VendorSerializer(instance=self.vendor).data,
            'on_time_delivery_rate': self.historical_performance.on_time_delivery_rate,
            'quality_rating_avg': self.historical_performance.quality_rating_avg,
            'average_response_time': self.historical_performance.average_response_time,
            'fulfillment_rate': self.historical_performance.fulfillment_rate
        }
        actual = HistoricalPerformanceSerializer(instance=self.historical_performance).data
        self.assertEqual(expected, actual)
