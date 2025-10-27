from django.db import models
from apps.accounts.models import User
from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.deals.models import Deal


class NotificationTemplate(models.Model):
    """Templates for different types of notifications"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
        ('webhook', 'Webhook'),
    ]
    
    NOTIFICATION_CATEGORY_CHOICES = [
        ('lead', 'Lead'),
        ('deal', 'Deal'),
        ('customer', 'Customer'),
        ('task', 'Task'),
        ('system', 'System'),
        ('marketing', 'Marketing'),
        ('support', 'Support'),
    ]
    
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=NOTIFICATION_CATEGORY_CHOICES)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    html_content = models.TextField(blank=True)
    variables = models.JSONField(default=list)  # Available template variables
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_templates'
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    
    def __str__(self):
        return self.name


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_enabled = models.BooleanField(default=True)
    email_lead_notifications = models.BooleanField(default=True)
    email_deal_notifications = models.BooleanField(default=True)
    email_customer_notifications = models.BooleanField(default=True)
    email_task_reminders = models.BooleanField(default=True)
    email_system_notifications = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)
    
    # SMS preferences
    sms_enabled = models.BooleanField(default=False)
    sms_urgent_only = models.BooleanField(default=True)
    sms_phone_number = models.CharField(max_length=20, blank=True)
    
    # Push notification preferences
    push_enabled = models.BooleanField(default=True)
    push_lead_notifications = models.BooleanField(default=True)
    push_deal_notifications = models.BooleanField(default=True)
    push_task_reminders = models.BooleanField(default=True)
    
    # In-app notification preferences
    in_app_enabled = models.BooleanField(default=True)
    in_app_all_categories = models.BooleanField(default=True)
    
    # Frequency settings
    digest_frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('never', 'Never'),
    ], default='immediate')
    
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"{self.user.full_name} Notification Preferences"


class NotificationQueue(models.Model):
    """Queue for pending notifications"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='queued_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queued_notifications')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Content
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    html_content = models.TextField(blank=True)
    
    # Delivery settings
    scheduled_at = models.DateTimeField(null=True, blank=True)
    max_retries = models.PositiveIntegerField(default=3)
    retry_count = models.PositiveIntegerField(default=0)
    
    # Related objects
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='queued_notifications')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='queued_notifications')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='queued_notifications')
    
    # Metadata
    context_data = models.JSONField(default=dict)  # Additional context for template rendering
    delivery_attempts = models.JSONField(default=list)  # Log of delivery attempts
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notification_queue'
        verbose_name = 'Queued Notification'
        verbose_name_plural = 'Queued Notifications'
        ordering = ['priority', 'scheduled_at', 'created_at']
    
    def __str__(self):
        return f"{self.template.name} -> {self.recipient.full_name}"


class NotificationDelivery(models.Model):
    """Record of notification deliveries"""
    
    STATUS_CHOICES = [
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
        ('webhook', 'Webhook'),
    ]
    
    queued_notification = models.ForeignKey(NotificationQueue, on_delete=models.CASCADE, related_name='deliveries')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    external_id = models.CharField(max_length=200, blank=True)  # ID from external service
    
    # Delivery details
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    error_code = models.CharField(max_length=50, blank=True)
    
    # Analytics
    delivery_time = models.PositiveIntegerField(null=True, blank=True)  # milliseconds
    response_data = models.JSONField(default=dict)  # Response from delivery service
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notification_deliveries'
        verbose_name = 'Notification Delivery'
        verbose_name_plural = 'Notification Deliveries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.queued_notification.template.name} - {self.status}"


class NotificationCampaign(models.Model):
    """Bulk notification campaigns"""
    
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
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='campaigns')
    
    # Targeting
    recipient_segment = models.JSONField(default=dict)  # Criteria for recipients
    recipient_list = models.JSONField(default=list)  # Specific recipient IDs
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Statistics
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    delivered_count = models.PositiveIntegerField(default=0)
    opened_count = models.PositiveIntegerField(default=0)
    clicked_count = models.PositiveIntegerField(default=0)
    bounced_count = models.PositiveIntegerField(default=0)
    unsubscribed_count = models.PositiveIntegerField(default=0)
    
    # Campaign settings
    is_test_campaign = models.BooleanField(default=False)
    test_recipients = models.JSONField(default=list)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_campaigns'
        verbose_name = 'Notification Campaign'
        verbose_name_plural = 'Notification Campaigns'
    
    def __str__(self):
        return self.name
    
    @property
    def delivery_rate(self):
        if self.sent_count == 0:
            return 0
        return (self.delivered_count / self.sent_count) * 100
    
    @property
    def open_rate(self):
        if self.delivered_count == 0:
            return 0
        return (self.opened_count / self.delivered_count) * 100
    
    @property
    def click_rate(self):
        if self.delivered_count == 0:
            return 0
        return (self.clicked_count / self.delivered_count) * 100


class NotificationSubscription(models.Model):
    """User subscriptions to notification types"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.CharField(max_length=20, choices=NotificationTemplate.NOTIFICATION_CATEGORY_CHOICES)
    is_subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_subscriptions'
        verbose_name = 'Notification Subscription'
        verbose_name_plural = 'Notification Subscriptions'
        unique_together = ['user', 'category']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.category}"
