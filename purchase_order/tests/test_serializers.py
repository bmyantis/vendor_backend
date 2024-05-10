from django.test import TestCase
from purchase_order.serializers import PurchaseOrderDeserializer, PurchaseOrderSerializer
from purchase_order.models import PurchaseOrder
from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class PurchaseOrderDeserializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", code="vendor_code")

    def test_valid_purchase_order_deserializer(self):
        data = {
            'vendor': str(self.vendor.id),
            'order_date': '2024-05-10T09:24:31.654820Z',
            'delivery_date': '2024-05-11T09:24:31.654820Z',
            'items': [],
            'quantity': 1,
            'status': PurchaseOrder.PENDING
        }
        serializer = PurchaseOrderDeserializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.vendor, self.vendor)

    def test_invalid_purchase_order_deserializer(self):
        # Invalid status transition
        purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date='2024-05-10T09:24:31.654820Z', delivery_date='2024-05-11T09:24:31.654820Z', items=[], quantity=1, status='pending')

        data = {
            'vendor': self.vendor.id,
            'order_date': '2024-05-10T09:24:31.654820Z',
            'delivery_date': '2024-05-11T09:24:31.654820Z',
            'items': [],
            'quantity': 1,
            'status': 'completed'  # Invalid status transition
        }
        serializer = PurchaseOrderDeserializer(instance=purchase_order, data=data)
        self.assertFalse(serializer.is_valid())

        # Test for missing vendor
        del data['vendor']
        serializer = PurchaseOrderDeserializer(instance=purchase_order, data=data)
        self.assertFalse(serializer.is_valid())


class PurchaseOrderSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", code="vendor_code")
        self.purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date='2024-05-10T09:24:31.654820Z', delivery_date='2024-05-11T09:24:31.654820Z', items=[], quantity=1, status='pending')

    def test_purchase_order_serializer(self):
        expected = {
            'id': str(self.purchase_order.id),
            'vendor': VendorSerializer(instance=self.vendor).data,
            'order_date': self.purchase_order.order_date,
            'delivery_date': self.purchase_order.delivery_date,
            'items': self.purchase_order.items,
            'quantity': self.purchase_order.quantity,
            'status': self.purchase_order.status,
            'number': self.purchase_order.number,
            'completed_date': self.purchase_order.completed_date,
            'acknowledgment_date': self.purchase_order.acknowledgment_date,
            'quality_rating': self.purchase_order.quality_rating,
            'issue_date': self.purchase_order.issue_date,
        }

        actual = PurchaseOrderSerializer(instance=self.purchase_order).data
        self.assertDictEqual(expected, actual)
