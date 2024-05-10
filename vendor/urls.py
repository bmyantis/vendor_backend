from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import VendorViewSet, HistoricalPerformanceViewSet

router = DefaultRouter()
router.register(r'(?P<vendor_id>[^/.]+)/performance', HistoricalPerformanceViewSet, basename='vendor-performance')

router.register(r'', VendorViewSet, basename='vendor')
urlpatterns = router.urls
