from django.db import models

from user_api.models import User


class SupplierCapabilityType(models.Model):
    """
        Work capability list of suppliers.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_capability_types_created'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_capability_types_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Capability Type"
        verbose_name_plural = "Capability Types"
        ordering = ["name"]


class Supplier(models.Model):
    """
        Supplier model to store supplier information.
    """
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    year_established = models.PositiveIntegerField(blank=True, null=True)
    total_workers = models.PositiveIntegerField(blank=True, null=True)
    total_factory_size = models.CharField(
        max_length=100, blank=True, null=True, help_text="e.g. 50,000 sq ft"
    )

    # --- Production Details ---
    main_products = models.CharField(
        max_length=255, blank=True, null=True, help_text="Main items produced"
    )
    production_capacity_units = models.PositiveIntegerField(
        blank=True, null=True, help_text="Production capacity in units/month"
    )
    capacity_utilization = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Utilization in %",
    )
    lead_time_days = models.PositiveIntegerField(
        blank=True, null=True, help_text="Average lead time in days"
    )
    payment_terms = models.CharField(
        max_length=100, blank=True, null=True, help_text="e.g. TT, LC, etc."
    )

    # --- Machinery & Equipment ---
    machinery_equipment = models.TextField(
        blank=True, null=True, help_text="List or details of key machines"
    )

    # --- Quality Control ---
    qc_inhouse_team = models.BooleanField(default=False)
    qc_third_party = models.BooleanField(default=False)
    qc_methods = models.JSONField(
        default=list,
        blank=True,
        help_text="QC types like Fabric Inspection, Metal Detection",
    )

    # --- Minimum Order Quantity (MOQ) ---
    moq_units_per_style = models.PositiveIntegerField(blank=True, null=True)
    moq_colors_per_style = models.PositiveIntegerField(blank=True, null=True)

    # --- Relations ---
    contact_persons = models.ManyToManyField(
        User,
        related_name="suppliers",
        blank=True,
    )
    capabilities = models.ManyToManyField(
        "SupplierCapabilityType",
        related_name="suppliers",
        blank=True,
        help_text="List of work capabilities.",
    )

    # certifications = models.JSONField(
    #     default=list,
    #     blank=True,
    #     help_text="List of compliance certificates like BSCI, SEDEX, WRAP, etc.", # noqa
    # )
    # --- Meta Info ---
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_created'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supplier_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.name
