from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from purchase_order.models import PurchaseOrder
from vendor.models import Vendor


class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", code="vendor_code")

    def test_generate_purchase_order_number(self):
        purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now(), items=[], quantity=1)
        self.assertIsNotNone(purchase_order.number)
        self.assertEqual(len(purchase_order.number), 12)

    def test_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now(), items=[], quantity=0)
            purchase_order.full_clean()

    def test_delivery_date_before_order_date(self):
        order_date = timezone.now()
        delivery_date = order_date - timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=order_date, delivery_date=delivery_date, items=[], quantity=1)
            purchase_order.full_clean()

    def test_str_representation(self):
        purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now(), items=[], quantity=1)
        self.assertEqual(str(purchase_order), purchase_order.number)
