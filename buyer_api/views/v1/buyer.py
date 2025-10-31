from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from buyer_api.models import Buyer

from buyer_api.serializers.buyer import BuyerSerializer


class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all().order_by("name")
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]
