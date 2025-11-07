from django.contrib import admin

from .models import Season, Department


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name', 'description',)
    readonly_fields = ("created_at", "updated_at",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name', 'description',)
    readonly_fields = ("created_at", "updated_at",)
