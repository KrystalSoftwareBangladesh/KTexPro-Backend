from rest_framework import serializers

from meta_api.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
