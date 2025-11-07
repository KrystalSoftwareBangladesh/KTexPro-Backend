from django.contrib import admin
from django.utils.html import format_html
from .models import StyleStatus


@admin.register(StyleStatus)
class StyleStatusAdmin(admin.ModelAdmin):
    list_display = [
        'get_hierarchy_display',
        'code',
        'get_color_badge',
        'order',
        'is_active',
        'get_children_count',
        'created_at'
    ]
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'parent')
        }),
        ('Display Settings', {
            'fields': ('order', 'color', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    # Optimize queries
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('parent').prefetch_related('children')

    # Custom display methods
    def get_hierarchy_display(self, obj):
        """Display status with indentation for child statuses"""
        if obj.parent:
            return format_html(
                '<span style="margin-left: 20px;">↳ {}</span>',
                obj.name
            )
        return format_html('<strong>{}</strong>', obj.name)
    get_hierarchy_display.short_description = 'Status Name'
    get_hierarchy_display.admin_order_field = 'name'

    def get_color_badge(self, obj):
        """Display color as a badge"""
        if obj.color:
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; '  # noqa
                'border-radius: 3px; font-size: 11px;">{}</span>',
                obj.color,
                obj.color
            )
        return '-'
    get_color_badge.short_description = 'Color'

    def get_children_count(self, obj):
        """Display count of child statuses"""
        if obj.parent is None:
            count = obj.children.count()
            if count > 0:
                return format_html(
                    '<span style="background-color: #e3f2fd; color: #1976d2; '
                    'padding: 2px 8px; border-radius: 10px; font-size: 11px;">{} sub-status(es)</span>',    # noqa
                    count
                )
            return '-'
        return '-'
    get_children_count.short_description = 'Children'

    # Custom actions
    actions = ['activate_statuses', 'deactivate_statuses']

    def activate_statuses(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request, f'{updated} status(es) activated successfully.')
    activate_statuses.short_description = 'Activate selected statuses'

    def deactivate_statuses(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request, f'{updated} status(es) deactivated successfully.')
    deactivate_statuses.short_description = 'Deactivate selected statuses'

    # Form validation
    def save_model(self, request, obj, form, change):
        # Prevent more than 2 levels of hierarchy
        if obj.parent and obj.parent.parent:
            from django.contrib import messages
            messages.error(
                request,
                'Cannot create more than 2 levels of hierarchy (parent > child only)'   # noqa
            )
            return
        super().save_model(request, obj, form, change)

    # Custom list display configurations
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Style Status Management'
        return super().changelist_view(request, extra_context=extra_context)
