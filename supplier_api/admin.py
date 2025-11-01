from django.contrib import admin
from .models import SupplierCapabilityType


@admin.register(SupplierCapabilityType)
class SupplierCapabilityTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        """
        Automatically set created_by and updated_by.
        """
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
