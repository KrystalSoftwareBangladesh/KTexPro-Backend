from rest_framework import viewsets, permissions

from supplier_api.models import Supplier

from supplier_api.serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """
        API endpoint for managing suppliers.
    """
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
