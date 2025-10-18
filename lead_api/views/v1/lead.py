from rest_framework import viewsets, permissions

from lead_api.models import Lead
from lead_api.serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing leads.
    Provides:
    - GET /leads/ → list all leads
    - POST /leads/ → create lead
    - GET /leads/{id}/ → retrieve single lead
    - PUT/PATCH /leads/{id}/ → update lead
    - DELETE /leads/{id}/ → delete lead
    """
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign logged-in user if provided
        serializer.save(assigned_to=self.request.user)
