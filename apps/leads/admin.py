from django.contrib import admin
from .models import Lead, LeadActivity, LeadScore, LeadSource, LeadCampaign


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'status', 'source', 'score', 'created_at')
    list_filter = ('status', 'source', 'created_at', 'assigned_to')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'activity_type', 'user', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('lead__first_name', 'lead__last_name', 'notes')


@admin.register(LeadScore)
class LeadScoreAdmin(admin.ModelAdmin):
    list_display = ('lead', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('lead__first_name', 'lead__last_name')


@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(LeadCampaign)
class LeadCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description')