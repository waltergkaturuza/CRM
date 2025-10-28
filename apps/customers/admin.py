from django.contrib import admin
from .models import Customer, CustomerSegment, CustomerNote, CustomerInteraction, CustomerContact


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'status', 'created_at')
    list_filter = ('status', 'customer_type', 'industry', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Business Information', {
            'fields': ('company_name', 'job_title', 'industry', 'company_size'),
            'classes': ('collapse',)
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('CRM Information', {
            'fields': ('assigned_to', 'source', 'tags', 'general_notes', 'status', 'customer_type')
        }),
        ('Financial', {
            'fields': ('lifetime_value', 'credit_limit', 'payment_terms'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('website', 'linkedin_url', 'twitter_handle', 'preferred_contact_method'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_contact_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'customer_count')
    search_fields = ('name', 'description')


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'title', 'user', 'is_private', 'created_at')
    list_filter = ('is_private', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'title', 'content')


@admin.register(CustomerInteraction)
class CustomerInteractionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'interaction_type', 'user', 'created_at')
    list_filter = ('interaction_type', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'notes')


@admin.register(CustomerContact)
class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ('customer', 'first_name', 'last_name', 'email', 'job_title', 'is_primary')
    list_filter = ('is_primary', 'department')
    search_fields = ('customer__first_name', 'customer__last_name', 'first_name', 'last_name', 'email')
