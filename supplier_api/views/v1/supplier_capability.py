from rest_framework import viewsets, permissions

from supplier_api.models import SupplierCapabilityType

from supplier_api.serializers import SupplierCapabilityTypeSerializer


class SupplierCapabilityTypeViewSet(viewsets.ModelViewSet):
    """
        API endpoint for managing supplier capability types.
    """
    queryset = SupplierCapabilityType.objects.all().order_by("name")
    serializer_class = SupplierCapabilityTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user,
                        updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
