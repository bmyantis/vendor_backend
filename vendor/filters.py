import django_filters

from .models import Vendor


class VendorFilter(django_filters.FilterSet):
    """filter for vendor model"""
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Vendor
        fields = ['name', ]
