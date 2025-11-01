from rest_framework import serializers

from supplier_api.models import SupplierCapabilityType


class SupplierCapabilityTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True)
    updated_by_name = serializers.CharField(
        source="updated_by.full_name", read_only=True)

    class Meta:
        model = SupplierCapabilityType
        fields = [
            "id", "name", "description", "is_active",
            "created_by", "updated_by", "created_by_name",
            "updated_by_name", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "created_at", "updated_at", "created_by", "updated_by"
        ]
