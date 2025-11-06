from rest_framework import serializers

from meta_api.models import Season


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'name', 'code', 'order', 'description']
        read_only_fields = ['id']
