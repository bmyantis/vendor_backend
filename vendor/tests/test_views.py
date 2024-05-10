from rest_framework.test import force_authenticate
from rest_framework.exceptions import NotFound

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from vendor.views import VendorViewSet, HistoricalPerformanceViewSet
from vendor.models import Vendor, HistoricalPerformance
from vendor.serializers import VendorSerializer, VendorDeserializer, HistoricalPerformanceSerializer

User = get_user_model()


class VendorViewSetTest(TestCase):
    def setUp(self):
        self.view = VendorViewSet
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='Contact 2', address='Address 2')
    
    def test_get_serializer_class_list_retrieve(self):
        viewset = VendorViewSet()
        viewset.action = 'list'
        self.assertEqual(viewset.get_serializer_class(), VendorSerializer)
        viewset.action = 'retrieve'
        self.assertEqual(viewset.get_serializer_class(), VendorSerializer)

    def test_get_serializer_class_other_actions(self):
        viewset = VendorViewSet()
        viewset.action = 'create'
        self.assertEqual(viewset.get_serializer_class(), VendorDeserializer)
        viewset.action = 'update'
        self.assertEqual(viewset.get_serializer_class(), VendorDeserializer)

    def test_get_queryset(self):
        view = self.view()
        request = self.factory.get('/api/vendors/')
        request.user = self.user
        view.request = request

        expected = [self.vendor1.id, self.vendor2.id]
        actual = view.get_queryset()

        self.assertQuerysetEqual(actual, expected, lambda item: item.id, ordered=False)

    def test_vendor_list(self):
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get(reverse('vendor-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual([self.vendor1.id, self.vendor2.id], [vendor['id'] for vendor in response.data])

    def test_vendor_retrieve(self):
        view = self.view.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('vendor-detail', kwargs={'pk': self.vendor1.pk}))
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.vendor1.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.vendor1.pk)

    def test_vendor_create(self):
        view = self.view.as_view({'post': 'create'})
        data = {'name': 'New Vendor', 'contact_details': 'New Contact', 'address': 'New Address'}
        request = self.factory.post(reverse('vendor-list'), data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Vendor.objects.count(), 3)

    def test_vendor_update(self):
        view = self.view.as_view({'patch': 'partial_update'})
        data = {'name': 'Updated Vendor', 'contact_details': 'Updated Contact', 'address': 'Updated Address'}
        request = self.factory.patch(reverse('vendor-detail', kwargs={'pk': self.vendor1.pk}), data=data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.vendor1.pk)
        self.assertEqual(response.status_code, 200)
        self.vendor1.refresh_from_db()
        self.assertEqual(self.vendor1.name, 'Updated Vendor')
        self.assertEqual(self.vendor1.contact_details, 'Updated Contact')
        self.assertEqual(self.vendor1.address, 'Updated Address')

    def test_vendor_delete(self):
        view = self.view.as_view({'delete': 'destroy'})
        request = self.factory.delete(reverse('vendor-detail', kwargs={'pk': self.vendor1.pk}))
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.vendor1.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_vendor_invalid_retrieve(self):
        view = self.view.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('vendor-detail', kwargs={'pk': 9999}))
        force_authenticate(request, user=self.user)
        response = view(request, pk=9999)
        self.assertEqual(response.status_code, 404)

    def test_vendor_invalid_update(self):
        view = self.view.as_view({'patch': 'partial_update'})
        data = {'name': 'Updated Vendor'}
        request = self.factory.patch(reverse('vendor-detail', kwargs={'pk': 9999}), data=data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=9999)
        self.assertEqual(response.status_code, 404)


class HistoricalPerformanceViewSetTest(TestCase):
    def setUp(self):
        self.view = HistoricalPerformanceViewSet
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.vendor = Vendor.objects.create(name='Vendor', contact_details='Contact', address='Address')
        self.performance1 = HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=0.95, quality_rating_avg=4.5, average_response_time=24, fulfillment_rate=0.98)
        self.performance2 = HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=0.90, quality_rating_avg=4.0, average_response_time=30, fulfillment_rate=0.95)

    def test_performance_list(self):
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get(reverse('vendor-list'))
        force_authenticate(request, user=self.user)
        response = view(request, vendor_id=self.vendor.pk)
        serializer = HistoricalPerformanceSerializer([self.performance1, self.performance2], many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_performance_list_invalid_vendor(self):
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get(reverse('vendor-list'))
        force_authenticate(request, user=self.user)
        response = view(request, vendor_id=999)
        self.assertEqual(response.status_code, 404)
