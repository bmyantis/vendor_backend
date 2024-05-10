from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from drf_model_serializer import serializers as drf_serializers

from .models import Vendor, HistoricalPerformance


class VendorDeserializer(drf_serializers.ModelSerializer):
    """Deserializer for Vendor model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='vendor.Vendor.id'), read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['code']
    

class VendorSerializer(drf_serializers.ModelSerializer):
    """Serializer for Vendor model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='vendor.Vendor.id'), read_only=True)
    
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only = fields


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for HistoricalPerformance model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='vendor.HistoricalPerformance.id'), read_only=True)
    vendor = VendorSerializer()

    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
