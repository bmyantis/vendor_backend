from model_bakery import baker
from django_filters import CharFilter
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from purchase_order.models import PurchaseOrder
from purchase_order.filters import PurchaseOrderFilter
from vendor.models import Vendor

User = get_user_model()


class PurchaseOrderFilterTestCase(TestCase):
    def test_filter_fields(self):
        # Create a test vendor
        self.vendor1 = baker.make(Vendor)
        self.vendor2 = baker.make(Vendor)
        current_time = timezone.now()
        one_day_later = current_time + timezone.timedelta(days=1)
        one_day_before = current_time - timezone.timedelta(days=1)

        # Create some sample pos for testing
        self.po1 = baker.make(PurchaseOrder, vendor=self.vendor1, order_date=one_day_before, delivery_date=one_day_later, items=[
            {
            "item_id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "quantity": 1,
            "unit_price": 50.0,
            "total_price": 500.0
            }
        ], quantity=3, status=PurchaseOrder.PENDING)

        self.po2 = baker.make(PurchaseOrder, vendor=self.vendor2, order_date=one_day_before, delivery_date=one_day_later, items=[
            {
            "item_id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "quantity": 1,
            "unit_price": 50.0,
            "total_price": 500.0
            }
        ], quantity=2, status=PurchaseOrder.PENDING)

        # Initialize the filter with data
        filter_data = {'number': self.po1.number, 'vendor': self.vendor1.id}
        filter_set = PurchaseOrderFilter(data=filter_data, queryset=PurchaseOrder.objects.all())

        # Check if filter set is valid
        self.assertTrue(filter_set.is_valid())

        # Check if expected filters are present
        self.assertIsInstance(filter_set.filters['number'], CharFilter)
        self.assertIsInstance(filter_set.filters['vendor'], CharFilter)

        # Check if filtering works as expected
        filtered_queryset = filter_set.qs
        self.assertEqual(filtered_queryset.count(), 1)
