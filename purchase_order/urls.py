from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet, AcknowledgeViewSet

from django.urls import path, include

router = DefaultRouter()

router.register(r'', PurchaseOrderViewSet, basename='purchase_order')
router.register(r'', AcknowledgeViewSet, basename='acknowledge')

urlpatterns = [
    path('', include(router.urls)),
]
