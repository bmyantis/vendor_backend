from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from vendor.models import Vendor
from purchase_order.models import PurchaseOrder

User = get_user_model()


class TestPurchaseOrderEndpoint(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.vendor = baker.make(Vendor)
        self.client.force_authenticate(self.user)
        self.po = baker.make(PurchaseOrder, vendor=self.vendor, acknowledgment_date=timezone.now())

    def test_get(self):
        url = '/api/purchase_orders/'
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post(self):
        url = '/api/purchase_orders/'
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        url = f'/api/purchase_orders/{self.po.id}/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        url = f'/api/purchase_orders/{self.po.id}/'
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ack(self):
        url = f'/api/purchase_orders/{self.po.id}/acknowledge/'
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
