from django.db import models
from django.core.validators import RegexValidator
from apps.accounts.models import User
from apps.customers.models import Customer


class Lead(models.Model):
    """Lead model for managing potential customers"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('nurturing', 'Nurturing'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('email_campaign', 'Email Campaign'),
        ('cold_call', 'Cold Call'),
        ('trade_show', 'Trade Show'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    company_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Lead Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    
    # Lead Scoring
    score = models.PositiveIntegerField(default=0)  # AI-calculated lead score
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timeline = models.CharField(max_length=50, blank=True)  # e.g., "Q1 2024", "Immediate"
    
    # Additional Information
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Conversion Tracking
    converted_to_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='converted_from_leads')
    conversion_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contact_date = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'leads'
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.company_name:
            return f"{self.first_name} {self.last_name} ({self.company_name})"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def days_since_created(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).days
    
    @property
    def is_hot(self):
        return self.score >= 80 and self.priority in ['high', 'urgent']


class LeadActivity(models.Model):
    """Track all lead activities and interactions"""
    
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('demo', 'Demo'),
        ('proposal', 'Proposal Sent'),
        ('follow_up', 'Follow Up'),
        ('note', 'Note Added'),
        ('status_change', 'Status Changed'),
        ('other', 'Other'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='lead_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    next_action = models.CharField(max_length=200, blank=True)
    next_action_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lead_activities'
        verbose_name = 'Lead Activity'
        verbose_name_plural = 'Lead Activities'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lead.full_name} - {self.get_activity_type_display()} - {self.subject}"


class LeadScore(models.Model):
    """Lead scoring criteria and history"""
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='score_history')
    score = models.PositiveIntegerField()
    factors = models.JSONField(default=dict)  # Breakdown of scoring factors
    calculated_by = models.CharField(max_length=50, default='ai')  # 'ai', 'manual', 'rule'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lead_scores'
        verbose_name = 'Lead Score'
        verbose_name_plural = 'Lead Scores'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lead.full_name} - Score: {self.score}"


class LeadSource(models.Model):
    """Track lead sources and their performance"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cost_per_lead = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lead_sources'
        verbose_name = 'Lead Source'
        verbose_name_plural = 'Lead Sources'
    
    def __str__(self):
        return self.name


class LeadCampaign(models.Model):
    """Marketing campaigns that generate leads"""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    campaign_type = models.CharField(max_length=50)  # email, social, paid_ads, etc.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_audience = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='planning')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lead_campaigns'
        verbose_name = 'Lead Campaign'
        verbose_name_plural = 'Lead Campaigns'
    
    def __str__(self):
        return self.name
    
    @property
    def leads_generated(self):
        return self.leads.count()
    
    @property
    def conversion_rate(self):
        total_leads = self.leads.count()
        if total_leads == 0:
            return 0
        converted_leads = self.leads.filter(converted_to_customer__isnull=False).count()
        return (converted_leads / total_leads) * 100
