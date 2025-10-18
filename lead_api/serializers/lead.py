from rest_framework import serializers

from lead_api.models import Lead


class LeadSerializer(serializers.ModelSerializer):
    buyer_type_display = serializers.CharField(
        source="get_buyer_type_display", read_only=True)
    status_display = serializers.CharField(
        source="get_status_display", read_only=True)
    source_display = serializers.CharField(
        source="get_source_display", read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"
