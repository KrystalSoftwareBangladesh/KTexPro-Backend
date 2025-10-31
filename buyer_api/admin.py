from django.contrib import admin
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "industry", "created_at")
    list_filter = ("industry", "created_at")
    search_fields = ("name", "email", "phone_number", "industry")
    filter_horizontal = ("contact_persons",)
    ordering = ("name",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Company Details", {
            "fields": (
                "name",
                "industry",
                "website",
                "email",
                "phone_number",
                "billing_address",
            )
        }),
        ("Contacts", {
            "fields": ("contact_persons",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )
