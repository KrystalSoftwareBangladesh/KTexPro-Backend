from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from django.db.models import Q
from style_api.models import StyleStatus

from style_api.serializers import (
    StyleStatusSerializer,
    StyleStatusCreateSerializer,
    StyleStatusTreeSerializer
)


class StyleStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing StyleStatus with hierarchical structure
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StyleStatus.objects.all()

        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)

        # Filter by parent (null for root level)
        parent = self.request.query_params.get('parent')
        if parent == 'null' or parent == '':
            queryset = queryset.filter(parent__isnull=True)
        elif parent is not None:
            queryset = queryset.filter(parent_id=parent)

        return queryset.select_related('parent').order_by('order', 'name')

    def get_serializer_class(self):
        if self.action == 'create':
            return StyleStatusCreateSerializer
        elif self.action == 'tree':
            return StyleStatusTreeSerializer
        return StyleStatusSerializer

    def list(self, request, *args, **kwargs):
        """
        Custom list to handle different response formats
        """
        # Check if flat list is requested
        flat = request.query_params.get('flat', 'false').lower() == 'true'

        if flat:
            return super().list(request, *args, **kwargs)

        # Return hierarchical structure by default
        root_statuses = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(root_statuses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Get complete status tree (only active items)
        """
        root_statuses = StyleStatus.objects.filter(
            parent__isnull=True,
            is_active=True
        ).order_by('order', 'name')

        serializer = self.get_serializer(root_statuses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def roots(self, request):
        """
        Get only root level statuses (no parent)
        """
        root_statuses = self.get_queryset().filter(parent__isnull=True)
        serializer = StyleStatusSerializer(root_statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """
        Get direct children of a specific status
        """
        status = self.get_object()
        children = status.children.all()
        serializer = StyleStatusSerializer(children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def descendants(self, request, pk=None):
        """
        Get all descendants of a specific status
        """
        status = self.get_object()

        def get_descendants(parent):
            descendants = []
            children = parent.children.all()
            for child in children:
                descendants.append(child)
                descendants.extend(get_descendants(child))
            return descendants

        all_descendants = get_descendants(status)
        serializer = StyleStatusSerializer(all_descendants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search statuses by name or code
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        statuses = self.get_queryset().filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )[:10]  # Limit results

        serializer = StyleStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
