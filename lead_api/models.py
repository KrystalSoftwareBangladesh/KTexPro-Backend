from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LeadSource(models.IntegerChoices):
    FACEBOOK = 1, "Facebook"
    INSTAGRAM = 2, "Instagram"
    WEBSITE = 3, "Website"
    EXHIBITION = 4, "Exhibition"
    REFERRAL = 5, "Referral"
    OTHER = 6, "Other"


class BuyerType(models.IntegerChoices):
    WHOLESALER = 1, "Wholesaler"
    RETAILER = 2, "Retailer"
    AGENT = 3, "Agent"
    BRAND = 4, "Brand"
    ONLINE_STORE = 5, "Online Store"


class LeadStatus(models.IntegerChoices):
    NEW = 1, "New"
    CONTACTED = 2, "Contacted"
    SAMPLE_SENT = 3, "Sample Sent"
    NEGOTIATION = 4, "Negotiation"
    CLOSED_WON = 5, "Closed Won"
    CLOSED_LOST = 6, "Closed Lost"


class Lead(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    buyer_type = models.PositiveSmallIntegerField(
        choices=BuyerType.choices, default=BuyerType.WHOLESALER
    )
    source = models.PositiveSmallIntegerField(
        choices=LeadSource.choices, default=LeadSource.FACEBOOK
    )
    status = models.PositiveSmallIntegerField(
        choices=LeadStatus.choices, default=LeadStatus.NEW
    )

    interested_products = models.JSONField(default=list, blank=True)
    target_price = models.CharField(max_length=50, blank=True, null=True)
    order_quantity = models.PositiveIntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )

    attachments = models.JSONField(default=list, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["buyer_type"]),
            models.Index(fields=["country"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_buyer_type_display()})"
