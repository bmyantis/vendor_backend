from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from drf_model_serializer import serializers as drf_serializers

from .models import PurchaseOrder
from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class PurchaseOrderDeserializer(drf_serializers.ModelSerializer):
    """Deserializer for PurchaseOrder model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='purchase_order.PurchaseOrder.id'), read_only=True)
    vendor = HashidSerializerCharField(source_field='vendor.Vendor.id', read_only=False)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['number']
    
    def validate_status(self, value):
        """Validates the status transition of the purchase order."""
        """Order of statuses: PENDING, COMPLETED, CANCELLED."""
        """COMPLETED/CANCELED orders cannot be changed to PENDING."""
        if self.instance:
            statuses = PurchaseOrder.STATUS_CHOICES
            old_status = self.instance.status
            new_status = value
            if statuses.index((old_status, old_status.capitalize())) > statuses.index((new_status, new_status.capitalize())):
                raise serializers.ValidationError("Invalid status transition.")
        return value
    
    def validate_vendor(self, value):
        """Validates the vendor field."""
        vendor_id = value
        vendor_instance = Vendor.objects.get(pk=vendor_id)
        return vendor_instance


class PurchaseOrderSerializer(drf_serializers.ModelSerializer):
    """Serializer for PurchaseOrder model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='purchase_order.PurchaseOrder.id'), read_only=True)
    vendor = VendorSerializer()
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only = fields
