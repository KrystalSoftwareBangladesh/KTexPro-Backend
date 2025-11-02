from rest_framework import serializers
from django.contrib.auth import get_user_model
from buyer_api.models import Buyer

from user_api.serializers.user import UserProfileSerializer

User = get_user_model()


class BuyerSerializer(serializers.ModelSerializer):
    contact_persons = UserProfileSerializer(many=True)
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True)
    updated_by_name = serializers.CharField(
        source="updated_by.full_name", read_only=True)

    class Meta:
        model = Buyer
        fields = [
            "id", "name", "industry", "website",
            "email", "phone_number", "billing_address",
            "contact_persons",
            "created_at", "created_by", "updated_by",
            "created_by_name", "updated_by_name",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        contact_persons_data = validated_data.pop("contact_persons", [])
        buyer = Buyer.objects.create(**validated_data)

        for person_data in contact_persons_data:
            user = UserProfileSerializer().create(person_data)
            buyer.contact_persons.add(user)

        return buyer

    def update(self, instance, validated_data):
        contact_persons_data = validated_data.pop("contact_persons", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if contact_persons_data is not None:
            instance.contact_persons.clear()

            for person_data in contact_persons_data:
                user = UserProfileSerializer().create(person_data)
                instance.contact_persons.add(user)

        return instance
