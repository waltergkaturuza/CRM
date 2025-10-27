from django.db import models
from django.contrib.auth.models import User
from apps.accounts.models import User
from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.deals.models import Deal


class Workflow(models.Model):
    """Automated workflows for CRM processes"""
    
    TRIGGER_TYPE_CHOICES = [
        ('customer_created', 'Customer Created'),
        ('customer_updated', 'Customer Updated'),
        ('lead_created', 'Lead Created'),
        ('lead_status_changed', 'Lead Status Changed'),
        ('deal_created', 'Deal Created'),
        ('deal_stage_changed', 'Deal Stage Changed'),
        ('email_received', 'Email Received'),
        ('task_completed', 'Task Completed'),
        ('date_based', 'Date Based'),
        ('manual', 'Manual Trigger'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_TYPE_CHOICES)
    trigger_conditions = models.JSONField(default=dict)  # Conditions for triggering
    actions = models.JSONField(default=list)  # List of actions to execute
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'workflows'
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
    
    def __str__(self):
        return self.name


class WorkflowExecution(models.Model):
    """Track workflow executions"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    trigger_data = models.JSONField(default=dict)  # Data that triggered the workflow
    execution_log = models.JSONField(default=list)  # Step-by-step execution log
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'workflow_executions'
        verbose_name = 'Workflow Execution'
        verbose_name_plural = 'Workflow Executions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.status} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"


class EmailTemplate(models.Model):
    """Email templates for automated communications"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('welcome', 'Welcome Email'),
        ('follow_up', 'Follow Up'),
        ('reminder', 'Reminder'),
        ('proposal', 'Proposal'),
        ('contract', 'Contract'),
        ('newsletter', 'Newsletter'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    variables = models.JSONField(default=list)  # Available template variables
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_templates'
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'
    
    def __str__(self):
        return self.name


class EmailCampaign(models.Model):
    """Email marketing campaigns"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='campaigns')
    recipient_segment = models.JSONField(default=dict)  # Criteria for recipients
    scheduled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    opened_count = models.PositiveIntegerField(default=0)
    clicked_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_campaigns'
        verbose_name = 'Email Campaign'
        verbose_name_plural = 'Email Campaigns'
    
    def __str__(self):
        return self.name
    
    @property
    def open_rate(self):
        if self.sent_count == 0:
            return 0
        return (self.opened_count / self.sent_count) * 100
    
    @property
    def click_rate(self):
        if self.sent_count == 0:
            return 0
        return (self.clicked_count / self.sent_count) * 100


class Task(models.Model):
    """Automated and manual tasks"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    TASK_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('follow_up', 'Follow Up'),
        ('proposal', 'Send Proposal'),
        ('contract', 'Contract Review'),
        ('custom', 'Custom Task'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Relationships
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    
    # Scheduling
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Automation
    is_automated = models.BooleanField(default=False)
    workflow_execution = models.ForeignKey(WorkflowExecution, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional fields
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['due_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status not in ['completed', 'cancelled']


class Notification(models.Model):
    """System notifications"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
        ('reminder', 'Reminder'),
    ]
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
        ('webhook', 'Webhook'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    
    # Recipients
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    recipient_email = models.EmailField(blank=True)  # For external notifications
    recipient_phone = models.CharField(max_length=20, blank=True)
    
    # Status and delivery
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related objects
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Additional data
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient}"


class AutomationRule(models.Model):
    """Rules for automated actions"""
    
    RULE_TYPE_CHOICES = [
        ('lead_scoring', 'Lead Scoring'),
        ('deal_assignment', 'Deal Assignment'),
        ('follow_up', 'Follow Up'),
        ('escalation', 'Escalation'),
        ('notification', 'Notification'),
        ('data_enrichment', 'Data Enrichment'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rule_type = models.CharField(max_length=30, choices=RULE_TYPE_CHOICES)
    conditions = models.JSONField(default=dict)  # Rule conditions
    actions = models.JSONField(default=list)  # Actions to take
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)  # Higher number = higher priority
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'automation_rules'
        verbose_name = 'Automation Rule'
        verbose_name_plural = 'Automation Rules'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.name


class AutomationLog(models.Model):
    """Log of automation rule executions"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ]
    
    rule = models.ForeignKey(AutomationRule, on_delete=models.CASCADE, related_name='execution_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    input_data = models.JSONField(default=dict)  # Input data for the rule
    output_data = models.JSONField(default=dict)  # Output/result of the rule
    error_message = models.TextField(blank=True)
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # milliseconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'automation_logs'
        verbose_name = 'Automation Log'
        verbose_name_plural = 'Automation Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rule.name} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
