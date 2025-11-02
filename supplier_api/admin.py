from django.contrib import admin

from .models import SupplierCapabilityType, Supplier


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


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "email",
        "phone_number",
        "year_established",
        "total_workers",
        "created_by",
        "updated_by",
        "created_at",
    )
    list_filter = ("country", "capabilities",)
    search_fields = ("name", "email", "phone_number", "country")
    filter_horizontal = ("contact_persons", "capabilities")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "name",
                "email",
                "phone_number",
                "country",
                "address",
                "year_established",
                "total_workers",
                "total_factory_size",
            )
        }),
        ("Production Details", {
            "fields": (
                "main_products",
                "production_capacity_units",
                "capacity_utilization",
                "lead_time_days",
                "payment_terms",
            )
        }),
        ("Machinery & Equipment", {
            "fields": ("machinery_equipment",)
        }),
        ("Quality Control", {
            "fields": ("qc_inhouse_team", "qc_third_party", "qc_methods")
        }),
        ("Minimum Order Quantity (MOQ)", {
            "fields": ("moq_units_per_style", "moq_colors_per_style")
        }),
        ("Relations", {
            "fields": ("contact_persons", "capabilities",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
