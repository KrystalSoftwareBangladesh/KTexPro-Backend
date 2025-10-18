from django.contrib import admin
from django.utils.html import format_html

from .models import Lead, LeadStatus, BuyerType


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # 🧾 List View Configuration
    list_display = (
        "id",
        "name",
        "contact_person",
        "country",
        "buyer_type_badge",
        "status_badge",
        "source_display",
        "assigned_to",
        "created_at",
    )

    # 🔍 Filters in right sidebar
    list_filter = (
        "status",
        "buyer_type",
        "source",
        "country",
        "is_active",
        "created_at",
    )

    # 🔎 Search by name/contact
    search_fields = (
        "name",
        "contact_person",
        "email",
        "phone",
        "whatsapp",
        "country",
        "city",
    )

    # 📅 Readonly auto fields
    readonly_fields = ("created_at", "updated_at")

    # 🧭 Default ordering
    ordering = ("-created_at",)

    # 🧩 Custom field display names
    list_display_links = ("id", "name")

    # 🧠 Custom admin display methods
    def buyer_type_badge(self, obj):
        color_map = {
            BuyerType.WHOLESALER: "#0288d1",
            BuyerType.RETAILER: "#2e7d32",
            BuyerType.AGENT: "#7b1fa2",
            BuyerType.BRAND: "#c2185b",
            BuyerType.ONLINE_STORE: "#f57c00",
        }
        color = color_map.get(obj.buyer_type, "#555")
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:6px;">{}</span>',    # noqa
            color,
            obj.get_buyer_type_display(),
        )

    buyer_type_badge.short_description = "Buyer Type"

    def status_badge(self, obj):
        color_map = {
            LeadStatus.NEW: "#0288d1",
            LeadStatus.CONTACTED: "#0288d1",
            LeadStatus.SAMPLE_SENT: "#f9a825",
            LeadStatus.NEGOTIATION: "#fb8c00",
            LeadStatus.CLOSED_WON: "#388e3c",
            LeadStatus.CLOSED_LOST: "#d32f2f",
        }
        color = color_map.get(obj.status, "#777")
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:6px;">{}</span>',    # noqa
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def source_display(self, obj):
        return obj.get_source_display()
    source_display.short_description = "Source"
