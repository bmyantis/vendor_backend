import logging
from datetime import datetime
from drf_rw_serializers import viewsets as drf_viewsets
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PurchaseOrderDeserializer, PurchaseOrderSerializer
from .filters import PurchaseOrderFilter
from .models import PurchaseOrder

logger = logging.getLogger(__name__)


class PurchaseOrderViewSet(drf_viewsets.ModelViewSet):
    """A viewset for viewing and editing purchase orders."""
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PurchaseOrderSerializer
        return PurchaseOrderDeserializer


class AcknowledgeViewSet(viewsets.ViewSet):
    """A viewset for acknowledging purchase orders."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            logger.error("Purchase order (%s) not found", pk)
            return Response({'error': 'Purchase order not found'}, status=404)
        
        vendor = purchase_order.vendor

        if purchase_order.acknowledgment_date:
            logger.error("This purchase order (%s) has already been acknowledged", pk)
            return Response({'error': 'This purchase order has already been acknowledged'}, status=400)

        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()

        # calculate the average response time of the vendor
        purchase_orders = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False, issue_date__isnull=False)
        total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in purchase_orders if po.acknowledgment_date and po.issue_date)
        average_response_time = total_response_time / purchase_orders.count() if purchase_orders.count() > 0 else 0

        vendor.historicalperformance_set.update_or_create(
            defaults={'average_response_time': average_response_time}
        )
        return Response({'message': 'Purchase order acknowledged successfully'}, status=200)
