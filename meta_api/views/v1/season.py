from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from meta_api.models import Season
from meta_api.serializers import SeasonSerializer


class SeasonListAPIView(generics.ListAPIView):
    """
        API endpoint to retrieve list of seasons

        Query Parameters:
        - is_active: Filter by active status (true/false)
        - search: Search in name, code, or description
        - ordering: Order by any field (e.g., order, name, -order)
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Filter fields
    # filterset_fields = ['is_active']

    # Search fields
    search_fields = ['name', 'code', 'description']

    # Ordering fields
    ordering_fields = ['order', 'name', 'code', 'created_at']
    ordering = ['order']  # Default ordering
