from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from vendor.models import Vendor

User = get_user_model()


class TestVendorEndpoint(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.vendor = baker.make(Vendor)
        self.client.force_authenticate(self.user)
        
    def test_get(self):
        url = '/api/verndors/'
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post(self):
        url = '/api/vendors/'
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        url = f'/api/vendors/{self.vendor.id}/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        url = f'/api/vendors/{self.vendor.id}/'
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ack(self):
        url = f'/api/vendors/{self.vendor.id}/performance/'
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
