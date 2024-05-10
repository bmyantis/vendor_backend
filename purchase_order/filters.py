import django_filters

from .models import PurchaseOrder


class PurchaseOrderFilter(django_filters.FilterSet):
    """filter for purchase order model"""
    number = django_filters.CharFilter(field_name='number', lookup_expr='exact') # Filter by PO number
    vendor = django_filters.CharFilter(field_name='vendor__id', lookup_expr='exact')  # Filter by vendor ID
    
    class Meta:
        model = PurchaseOrder
        fields = ['number', 'vendor' ]
