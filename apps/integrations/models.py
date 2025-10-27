from django.db import models
from apps.accounts.models import User


class Integration(models.Model):
    """Third-party integrations"""
    
    INTEGRATION_TYPE_CHOICES = [
        ('email', 'Email Service'),
        ('calendar', 'Calendar'),
        ('crm', 'CRM System'),
        ('marketing', 'Marketing Platform'),
        ('support', 'Support System'),
        ('social', 'Social Media'),
        ('analytics', 'Analytics'),
        ('payment', 'Payment Gateway'),
        ('webhook', 'Webhook'),
        ('api', 'API Integration'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('pending', 'Pending Setup'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    provider = models.CharField(max_length=100)  # e.g., 'Gmail', 'Outlook', 'Salesforce'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    configuration = models.JSONField(default=dict)  # Integration-specific settings
    credentials = models.JSONField(default=dict)  # Encrypted credentials
    webhook_url = models.URLField(blank=True)
    api_endpoint = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_frequency = models.PositiveIntegerField(default=3600)  # seconds
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integrations'
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'
    
    def __str__(self):
        return f"{self.name} ({self.provider})"


class IntegrationLog(models.Model):
    """Log of integration activities"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField()
    details = models.JSONField(default=dict)
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # milliseconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'integration_logs'
        verbose_name = 'Integration Log'
        verbose_name_plural = 'Integration Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.integration.name} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class EmailIntegration(models.Model):
    """Email service integrations"""
    
    SERVICE_CHOICES = [
        ('gmail', 'Gmail'),
        ('outlook', 'Microsoft Outlook'),
        ('yahoo', 'Yahoo Mail'),
        ('custom_smtp', 'Custom SMTP'),
    ]
    
    integration = models.OneToOneField(Integration, on_delete=models.CASCADE, related_name='email_integration')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    email_address = models.EmailField()
    smtp_server = models.CharField(max_length=200, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    imap_server = models.CharField(max_length=200, blank=True)
    imap_port = models.PositiveIntegerField(null=True, blank=True)
    sync_sent_emails = models.BooleanField(default=True)
    sync_received_emails = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'email_integrations'
        verbose_name = 'Email Integration'
        verbose_name_plural = 'Email Integrations'
    
    def __str__(self):
        return f"{self.service} - {self.email_address}"


class CalendarIntegration(models.Model):
    """Calendar service integrations"""
    
    SERVICE_CHOICES = [
        ('google', 'Google Calendar'),
        ('outlook', 'Microsoft Outlook'),
        ('apple', 'Apple Calendar'),
        ('caldav', 'CalDAV'),
    ]
    
    integration = models.OneToOneField(Integration, on_delete=models.CASCADE, related_name='calendar_integration')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    calendar_id = models.CharField(max_length=200)
    sync_events = models.BooleanField(default=True)
    create_events = models.BooleanField(default=True)
    update_events = models.BooleanField(default=True)
    delete_events = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'calendar_integrations'
        verbose_name = 'Calendar Integration'
        verbose_name_plural = 'Calendar Integrations'
    
    def __str__(self):
        return f"{self.service} - {self.calendar_id}"


class WebhookIntegration(models.Model):
    """Webhook integrations"""
    
    integration = models.OneToOneField(Integration, on_delete=models.CASCADE, related_name='webhook_integration')
    webhook_url = models.URLField()
    secret_key = models.CharField(max_length=200, blank=True)
    events = models.JSONField(default=list)  # Events to listen for
    is_active = models.BooleanField(default=True)
    retry_count = models.PositiveIntegerField(default=3)
    timeout_seconds = models.PositiveIntegerField(default=30)
    
    class Meta:
        db_table = 'webhook_integrations'
        verbose_name = 'Webhook Integration'
        verbose_name_plural = 'Webhook Integrations'
    
    def __str__(self):
        return f"Webhook - {self.webhook_url}"


class APIIntegration(models.Model):
    """API integrations"""
    
    AUTH_TYPE_CHOICES = [
        ('none', 'No Authentication'),
        ('api_key', 'API Key'),
        ('oauth2', 'OAuth 2.0'),
        ('basic', 'Basic Authentication'),
        ('bearer', 'Bearer Token'),
    ]
    
    integration = models.OneToOneField(Integration, on_delete=models.CASCADE, related_name='api_integration')
    base_url = models.URLField()
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE_CHOICES)
    api_key = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=200, blank=True)
    bearer_token = models.CharField(max_length=500, blank=True)
    headers = models.JSONField(default=dict)  # Additional headers
    rate_limit = models.PositiveIntegerField(null=True, blank=True)  # requests per minute
    
    class Meta:
        db_table = 'api_integrations'
        verbose_name = 'API Integration'
        verbose_name_plural = 'API Integrations'
    
    def __str__(self):
        return f"API - {self.base_url}"


class DataSync(models.Model):
    """Data synchronization between systems"""
    
    SYNC_TYPE_CHOICES = [
        ('bidirectional', 'Bidirectional'),
        ('import', 'Import Only'),
        ('export', 'Export Only'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('error', 'Error'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    source_integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='source_syncs')
    target_integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='target_syncs')
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    field_mapping = models.JSONField(default=dict)  # Field mapping between systems
    sync_frequency = models.PositiveIntegerField(default=3600)  # seconds
    last_sync = models.DateTimeField(null=True, blank=True)
    next_sync = models.DateTimeField(null=True, blank=True)
    sync_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'data_syncs'
        verbose_name = 'Data Sync'
        verbose_name_plural = 'Data Syncs'
    
    def __str__(self):
        return f"{self.name} ({self.source_integration.name} -> {self.target_integration.name})"


class SyncLog(models.Model):
    """Data sync execution logs"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('partial', 'Partial Success'),
    ]
    
    data_sync = models.ForeignKey(DataSync, on_delete=models.CASCADE, related_name='sync_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    records_processed = models.PositiveIntegerField(default=0)
    records_successful = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # milliseconds
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'sync_logs'
        verbose_name = 'Sync Log'
        verbose_name_plural = 'Sync Logs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.data_sync.name} - {self.status} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"
