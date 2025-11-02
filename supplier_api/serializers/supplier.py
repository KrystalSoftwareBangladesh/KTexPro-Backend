from django.contrib.auth import get_user_model

from rest_framework import serializers

from supplier_api.models import Supplier, SupplierCapabilityType

from supplier_api.serializers import SupplierCapabilityTypeSerializer
from user_api.serializers import UserProfileSerializer

User = get_user_model()


class SupplierSerializer(serializers.ModelSerializer):
    contact_persons = UserProfileSerializer(many=True)
    capabilities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SupplierCapabilityType.objects.filter(is_active=True)
    )
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True)
    updated_by_name = serializers.CharField(
        source="updated_by.full_name", read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "id", "name", "email", "phone_number", "country",
            "address", "year_established", "total_workers",
            "total_factory_size", "main_products",
            "production_capacity_units", "capacity_utilization",
            "lead_time_days", "payment_terms", "machinery_equipment",
            "qc_inhouse_team", "qc_third_party", "qc_methods",
            "moq_units_per_style", "moq_colors_per_style",
            "capabilities", "contact_persons",
            "created_by", "updated_by", "created_by_name", "updated_by_name",
            "created_at", "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["capabilities"] = SupplierCapabilityTypeSerializer(
            instance.capabilities.all(), many=True).data
        return data

    def create(self, validated_data):
        contact_persons_data = validated_data.pop("contact_persons", [])
        capabilities_data = validated_data.pop("capabilities", [])
        supplier = Supplier.objects.create(**validated_data)

        for person_data in contact_persons_data:
            user = UserProfileSerializer().create(person_data)
            supplier.contact_persons.add(user)

        supplier.capabilities.set(capabilities_data)

        return supplier

    def update(self, instance, validated_data):
        contact_persons_data = validated_data.pop("contact_persons", None)
        capabilities_data = validated_data.pop("capabilities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if contact_persons_data is not None:
            instance.contact_persons.clear()

            for person_data in contact_persons_data:
                user = UserProfileSerializer().create(person_data)
                instance.contact_persons.add(user)

        if contact_persons_data is not None:
            instance.contact_persons.clear()
            for person_data in contact_persons_data:
                user = UserProfileSerializer().create(person_data)
                instance.contact_persons.add(user)

        if capabilities_data is not None:
            instance.capabilities.set(capabilities_data)
        return instance
