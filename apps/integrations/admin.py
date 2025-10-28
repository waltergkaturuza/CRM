from django.contrib import admin
from .models import Integration


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'integration_type', 'is_active', 'created_at')
    list_filter = ('integration_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'integration_type', 'description')
        }),
        ('Configuration', {
            'fields': ('config', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
