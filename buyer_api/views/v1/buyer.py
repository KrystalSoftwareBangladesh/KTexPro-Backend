from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiRequest

from buyer_api.models import Buyer

from buyer_api.serializers import BuyerSerializer
from user_api.serializers import UserProfileSerializer


class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all().order_by("name")
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @extend_schema(
        request=OpenApiRequest(UserProfileSerializer(many=True)),
        responses={201: BuyerSerializer},
        description="Add multiple contact persons to an existing buyer."
    )
    @action(detail=True, methods=["post"], url_path="add-contact-persons")
    def add_contact_person(self, request, pk=None):
        buyer = self.get_object()

        serializer = UserProfileSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        created_users = []

        for person_data in serializer.validated_data:
            user = UserProfileSerializer().create(person_data)
            buyer.contact_persons.add(user)
            created_users.append(user)

        buyer.save()
        buyer_data = BuyerSerializer(buyer).data

        return Response(buyer_data, status=status.HTTP_201_CREATED)
