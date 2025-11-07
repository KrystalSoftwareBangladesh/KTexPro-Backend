# serializers.py
from rest_framework import serializers
from style_api.models import StyleStatus


class StyleStatusSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    parent_code = serializers.CharField(source='parent.code', read_only=True)

    class Meta:
        model = StyleStatus
        fields = [
            'id', 'name', 'code', 'parent', 'parent_name', 'parent_code',
            'order', 'is_active', 'description', 'color',
            'children', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'children']

    def get_children(self, obj):
        """Recursively get all children statuses"""
        children = obj.children.filter(is_active=True).order_by('order')
        serializer = StyleStatusSerializer(
            children, many=True, context=self.context)
        return serializer.data

    def validate_parent(self, value):
        """Validate that parent exists and doesn't create circular reference"""
        if value and value == self.instance:
            raise serializers.ValidationError(
                "A status cannot be its own parent.")
        return value

    def validate_code(self, value):
        """Validate code uniqueness"""
        if self.instance and self.instance.code == value:
            return value

        if StyleStatus.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "A status with this code already exists.")
        return value


class StyleStatusCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating statuses (without children field for performance)
    """
    class Meta:
        model = StyleStatus
        fields = [
            'id', 'name', 'code', 'parent', 'order',
            'is_active', 'description', 'color'
        ]
        read_only_fields = ['id']


class StyleStatusTreeSerializer(serializers.ModelSerializer):
    """Serializer for tree structure (only active items)"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = StyleStatus
        fields = ['id', 'name', 'code', 'color', 'children', 'order']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('order')
        return StyleStatusTreeSerializer(children, many=True).data
