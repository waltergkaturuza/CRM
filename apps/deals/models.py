from django.db import models
from apps.accounts.models import User
from apps.customers.models import Customer
from apps.leads.models import Lead


class Deal(models.Model):
    """Deal/Opportunity model for sales pipeline management"""
    
    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Financial Information
    value = models.DecimalField(max_digits=12, decimal_places=2)
    probability = models.PositiveIntegerField(default=0)  # 0-100%
    expected_close_date = models.DateTimeField()
    actual_close_date = models.DateTimeField(null=True, blank=True)
    
    # Relationships
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='deals')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_deals')
    
    # Additional Information
    source = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    
    # Competition & Risk
    competitors = models.TextField(blank=True)
    risks = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'deals'
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.customer.full_name}"
    
    @property
    def weighted_value(self):
        """Calculate weighted value based on probability"""
        return (self.value * self.probability) / 100
    
    @property
    def days_to_close(self):
        from django.utils import timezone
        if self.actual_close_date:
            return None
        return (self.expected_close_date - timezone.now()).days
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.expected_close_date < timezone.now() and not self.actual_close_date
    
    @property
    def is_closed(self):
        return self.stage in ['closed_won', 'closed_lost']


class DealActivity(models.Model):
    """Track all deal activities and interactions"""
    
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('demo', 'Demo'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('follow_up', 'Follow Up'),
        ('note', 'Note Added'),
        ('stage_change', 'Stage Changed'),
        ('other', 'Other'),
    ]
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='deal_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    next_action = models.CharField(max_length=200, blank=True)
    next_action_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'deal_activities'
        verbose_name = 'Deal Activity'
        verbose_name_plural = 'Deal Activities'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.deal.name} - {self.get_activity_type_display()} - {self.subject}"


class DealProduct(models.Model):
    """Products/services associated with deals"""
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'deal_products'
        verbose_name = 'Deal Product'
        verbose_name_plural = 'Deal Products'
    
    def __str__(self):
        return f"{self.deal.name} - {self.name}"
    
    @property
    def total_price(self):
        discount_amount = (self.unit_price * self.discount_percentage) / 100
        discounted_price = self.unit_price - discount_amount
        return discounted_price * self.quantity


class DealStage(models.Model):
    """Customizable deal stages for different sales processes"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    probability = models.PositiveIntegerField(default=0)  # Default probability for this stage
    is_closed = models.BooleanField(default=False)
    is_won = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'deal_stages'
        verbose_name = 'Deal Stage'
        verbose_name_plural = 'Deal Stages'
        ordering = ['order']
        unique_together = ['name', 'order']
    
    def __str__(self):
        return self.name


class SalesPipeline(models.Model):
    """Sales pipeline configuration"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    stages = models.ManyToManyField(DealStage, related_name='pipelines')
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sales_pipelines'
        verbose_name = 'Sales Pipeline'
        verbose_name_plural = 'Sales Pipelines'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one default pipeline
        if self.is_default:
            SalesPipeline.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class DealForecast(models.Model):
    """Sales forecasting data"""
    
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    forecasted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'deal_forecasts'
        verbose_name = 'Deal Forecast'
        verbose_name_plural = 'Deal Forecasts'
        unique_together = ['period_type', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.period_type.title()} Forecast - {self.period_start.strftime('%Y-%m')}"
    
    @property
    def accuracy(self):
        if not self.actual_amount:
            return None
        if self.forecasted_amount == 0:
            return 0
        return abs(self.actual_amount - self.forecasted_amount) / self.forecasted_amount * 100
