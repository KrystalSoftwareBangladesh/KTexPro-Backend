from rest_framework import serializers
from django.contrib.auth import get_user_model
from buyer_api.models import Buyer

from user_api.serializers.user import UserProfileSerializer

User = get_user_model()


class BuyerSerializer(serializers.ModelSerializer):
    contact_persons = UserProfileSerializer(many=True)
    # contact_persons_ids = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source="contact_persons"
    # )

    class Meta:
        model = Buyer
        fields = [
            "id",
            "name",
            "industry",
            "website",
            "email",
            "phone_number",
            "billing_address",
            "contact_persons",
            # "contact_persons_ids",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        print("Welcome to create buyer serializer...")
        contact_persons_data = validated_data.pop("contact_persons", [])
        buyer = Buyer.objects.create(**validated_data)
        for person_data in contact_persons_data:
            user = UserProfileSerializer().create(person_data)
            print("User...", user)
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
