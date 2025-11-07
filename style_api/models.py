from django.db import models


class StyleStatus(models.Model):
    """
    Style Status with parent-child hierarchy
    Parent statuses are main statuses, child statuses are sub-statuses
    """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Order in which statuses appear")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Hex color code for UI display (e.g., #FF5733)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'style_statuses'
        ordering = ['order', 'name']
        verbose_name = 'Style Status'
        verbose_name_plural = 'Style Statuses'
        indexes = [
            models.Index(fields=['parent', 'order']),
            models.Index(fields=['code', 'is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'name'],
                name='unique_status_name_per_parent'
            )
        ]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def is_parent(self):
        """Check if this is a parent status"""
        return self.parent is None

    def is_child(self):
        """Check if this is a child status"""
        return self.parent is not None

    def get_level(self):
        """Get the level in hierarchy (0 for parent, 1 for child)"""
        return 0 if self.is_parent() else 1

    def get_full_path(self):
        """Get full path of status"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_children_count(self):
        """Get count of child statuses"""
        return self.children.filter(is_active=True).count()

    @classmethod
    def get_parent_statuses(cls):
        """Get all parent statuses"""
        return cls.objects.filter(parent=None, is_active=True).order_by('order')  # noqa

    @classmethod
    def get_child_statuses(cls, parent_id=None):
        """Get child statuses, optionally filtered by parent"""
        queryset = cls.objects.filter(parent__isnull=False, is_active=True)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset.order_by('order')

    def save(self, *args, **kwargs):
        # Prevent more than 2 levels of hierarchy
        if self.parent and self.parent.parent:
            raise ValueError(
                "Cannot create more than 2 levels of hierarchy (parent > child only)")  # noqa
        super().save(*args, **kwargs)
