import json
from unittest.mock import patch
from model_bakery import baker
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from purchase_order.models import PurchaseOrder
from purchase_order.views import PurchaseOrderViewSet, AcknowledgeViewSet
from purchase_order.serializers import PurchaseOrderDeserializer, PurchaseOrderSerializer
from purchase_order.views import PurchaseOrderViewSet
from vendor.models import Vendor

User = get_user_model()


class PurchaseOrderViewSetTestCase(TestCase):
    def setUp(self):
        self.view = PurchaseOrderViewSet
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='test')
        # Create a test vendor
        self.vendor1 = baker.make(Vendor)
        self.vendor2 = baker.make(Vendor)
        current_time = timezone.now()
        self.one_day_later = current_time + timezone.timedelta(days=1)
        self.one_day_before = current_time - timezone.timedelta(days=1)

        # Create some sample pos for testing
        self.po1 = baker.make(PurchaseOrder, vendor=self.vendor1, order_date=self.one_day_before, delivery_date=self.one_day_later, items=[
            {
            "item_id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "quantity": 1,
            "unit_price": 50.0,
            "total_price": 500.0
            }
        ], quantity=3, status=PurchaseOrder.PENDING)

        self.po2 = baker.make(PurchaseOrder, vendor=self.vendor2, order_date=self.one_day_before, delivery_date=self.one_day_later, items=[
            {
            "item_id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "quantity": 1,
            "unit_price": 50.0,
            "total_price": 500.0
            }
        ], quantity=2, status=PurchaseOrder.PENDING)

    def test_get_serializer_class_list_retrieve(self):
        viewset = PurchaseOrderViewSet()
        viewset.action = 'list'
        self.assertEqual(viewset.get_serializer_class(), PurchaseOrderSerializer)
        viewset.action = 'retrieve'
        self.assertEqual(viewset.get_serializer_class(), PurchaseOrderSerializer)

    def test_get_serializer_class_other_actions(self):
        viewset = PurchaseOrderViewSet()
        viewset.action = 'create'
        self.assertEqual(viewset.get_serializer_class(), PurchaseOrderDeserializer)
        viewset.action = 'update'
        self.assertEqual(viewset.get_serializer_class(), PurchaseOrderDeserializer)

    def test_get_queryset(self):
        view = self.view()
        request = self.factory.get('/api/purchase_orders/')
        request.user = self.user
        view.request = request

        expected = [self.po1.id, self.po2.id]
        actual = view.get_queryset()

        self.assertQuerysetEqual(actual, expected, lambda item: item.id, ordered=False)

    def test_list(self):
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get(reverse('purchase_order-list'))
        force_authenticate(request, self.user)
        view.request = request
        response = view(request)

        self.assertEqual(len(response.data), 2)
        self.assertEqual([self.po1.id, self.po2.id], [po['id'] for po in response.data])
    
    def test_post(self):
        view = self.view.as_view({'post': 'create'})
        data = {
            "vendor": str(self.vendor1.id),
            "order_date": self.one_day_before,
            "delivery_date": self.one_day_later,
            "items": [
                {
                "item_id": 1,
                "name": "Product A",
                "description": "Description of Product A",
                "quantity": 1,
                "unit_price": 50.0,
                "total_price": 500.0
                }
            ],
            "quantity": 1,
            "status": "pending"
        }

        request = self.factory.post(reverse('purchase_order-list'), data=data, format='json')
        force_authenticate(request, self.user)
        view.request = request
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete(self):
        view = self.view.as_view({'delete': 'destroy'})
        request = self.factory.delete(reverse('purchase_order-detail', kwargs={'pk': self.po1.pk}))
        force_authenticate(request, self.user)
        response = view(request, pk=self.po1.pk)
        self.assertEqual(response.status_code, 204) 

    def test_update(self):
        new_status = PurchaseOrder.CANCELED
        new_issue_date = timezone.now()
        view = self.view.as_view({'patch': 'partial_update'})
        data = {
            "status": new_status,
            "issue_date": new_issue_date,
        }
        request = self.factory.patch(reverse('purchase_order-detail', kwargs={'pk': self.po1.pk}), data=data)
        force_authenticate(request, self.user)
        response = view(request, pk=self.po1.pk)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

        # Ensure response data matches the updated data
        self.assertEqual(response.data['status'], new_status)
        self.assertEqual(response.data['issue_date'], new_issue_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        # Refresh the purchase order object from the database
        self.po1.refresh_from_db()

        # Ensure the object was updated in the database
        self.assertEqual(self.po1.status, new_status)
        self.assertEqual(self.po1.issue_date, new_issue_date)

    def test_get_detail(self):
        view = self.view.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('purchase_order-detail', kwargs={'pk': self.po1.pk}))
        force_authenticate(request, self.user)
        response = view(request, pk=self.po1.pk)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code,  status.HTTP_200_OK) 
        self.assertEqual(response.data['id'], self.po1.pk)

class AcknowledgeViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.vendor = baker.make(Vendor)
        self.purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now(), items=[], quantity=1)

    @patch('purchase_order.views.datetime')
    def test_acknowledge_successful(self, mock_datetime):
        mock_now = timezone.now()
        mock_datetime.now.return_value = mock_now

        viewset = AcknowledgeViewSet()
        request = self.factory.post('/acknowledge/', {'pk': self.purchase_order.pk})
        response = viewset.acknowledge(request, pk=self.purchase_order.pk)

        # Ensure status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.acknowledgment_date, mock_now)

    def test_acknowledge_already_acknowledged(self):
        self.purchase_order.acknowledgment_date = timezone.now()
        self.purchase_order.save()

        viewset = AcknowledgeViewSet()
        request = self.factory.post('/acknowledge/', {'pk': self.purchase_order.pk})
        response = viewset.acknowledge(request, pk=self.purchase_order.pk)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This purchase order has already been acknowledged')
