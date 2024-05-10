from django.test import TestCase
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from purchase_order.models import PurchaseOrder, Vendor


class SignalsTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")
        current_time = timezone.now()
        self.one_day_later = current_time + timezone.timedelta(days=1)
        self.one_day_before = current_time - timezone.timedelta(days=1)

    def test_post_save_signal(self):
        # Ensure post-save signal updates vendor historical performance correctly
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            order_date=self.one_day_before,
            delivery_date=self.one_day_later,
            quantity=1,
            items=[],
            status=PurchaseOrder.COMPLETED,
            quality_rating=4.5
        )
        post_save.send(sender=PurchaseOrder, instance=self.purchase_order, created=False)
        vendor_performance = self.vendor.historicalperformance_set.first()
        self.assertIsNotNone(vendor_performance)
        self.assertEqual(vendor_performance.on_time_delivery_rate, 100)
        self.assertEqual(vendor_performance.quality_rating_avg, 4.5)

    def test_pre_save_signal(self):
        # Ensure pre-save signal updates vendor historical performance correctly
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            order_date=self.one_day_before,
            delivery_date=self.one_day_later,
            quantity=1,
            items=[],
            status=PurchaseOrder.CANCELED,
            quality_rating=4.5,
            issue_date=timezone.now()
        )
        pre_save.send(sender=PurchaseOrder, instance=self.purchase_order)
        vendor_performance = self.vendor.historicalperformance_set.first()
        self.assertIsNotNone(vendor_performance)
        self.assertEqual(vendor_performance.fulfillment_rate, 0)

    def test_pre_save_signal_status_change(self):
        # Ensure pre-save signal updates vendor historical performance correctly on status change
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            order_date=self.one_day_before,
            delivery_date=self.one_day_before,
            quantity=1,
            items=[],
            status=PurchaseOrder.COMPLETED,
            quality_rating=4.5,
            issue_date=timezone.now()
        )
        pre_save.send(sender=PurchaseOrder, instance=self.purchase_order)
        vendor_performance = self.vendor.historicalperformance_set.first()
        self.assertIsNotNone(vendor_performance)
        self.assertEqual(vendor_performance.fulfillment_rate, 0)
        self.assertEqual(vendor_performance.quality_rating_avg, 4.5)
