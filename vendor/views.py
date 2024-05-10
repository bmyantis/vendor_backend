import logging
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from drf_rw_serializers import viewsets as drf_viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import VendorDeserializer, VendorSerializer, HistoricalPerformanceSerializer
from .filters import VendorFilter
from .models import Vendor, HistoricalPerformance

logger = logging.getLogger(__name__)


class VendorViewSet(drf_viewsets.ModelViewSet):
    """A viewset for viewing and editing vendors."""
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_class = VendorFilter
    queryset = Vendor.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action in ['list', 'retrieve']:
            return VendorSerializer
        return VendorDeserializer


class HistoricalPerformanceViewSet(viewsets.ViewSet):
    """A viewset for viewing historical performance of a vendor."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistoricalPerformanceSerializer

    def list(self, request, vendor_id=None):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            performances = HistoricalPerformance.objects.filter(vendor=vendor)
            serializer = self.serializer_class(performances, many=True)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            logger.error("vendor (%s) not found", vendor_id)
            return Response({'error': 'Vendor not found'}, status=404)
