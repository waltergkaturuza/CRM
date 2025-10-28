from django.contrib import admin
from .models import Workflow, WorkflowExecution, EmailTemplate, EmailCampaign, Task, AutomationRule, AutomationLog


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(WorkflowExecution)
class WorkflowExecutionAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'status', 'started_at', 'completed_at')
    list_filter = ('status', 'started_at')
    search_fields = ('workflow__name',)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'subject')


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')


@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(AutomationLog)
class AutomationLogAdmin(admin.ModelAdmin):
    list_display = ('rule', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('rule__name',)
