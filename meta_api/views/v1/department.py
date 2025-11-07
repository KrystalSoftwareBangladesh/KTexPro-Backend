from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from meta_api.models import Department
from meta_api.serializers import DepartmentSerializer


class DepartmentListAPIView(generics.ListAPIView):
    """
        API endpoint to retrieve list of departments

        Query Parameters:
        - search: Search in name, or description
        - ordering: Order by any field (e.g., name)
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Search fields
    search_fields = ['name', 'description']
