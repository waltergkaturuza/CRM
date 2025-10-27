from django.db import models
from django.core.validators import RegexValidator
from apps.accounts.models import User


class Customer(models.Model):
    """Main Customer model"""
    
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('nonprofit', 'Non-Profit'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('lead', 'Lead'),
        ('churned', 'Churned'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    
    # Customer Classification
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospect')
    
    # Business Information (for business customers)
    company_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)  # e.g., "1-10", "11-50", "51-200", etc.
    
    # Address Information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # CRM Fields
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_customers')
    source = models.CharField(max_length=100, blank=True)  # How they found us
    tags = models.JSONField(default=list, blank=True)  # Flexible tagging system
    notes = models.TextField(blank=True)
    
    # Financial Information
    lifetime_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.CharField(max_length=50, blank=True)
    
    # Social Media & Communication
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    ], default='email')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contact_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.company_name:
            return f"{self.first_name} {self.last_name} ({self.company_name})"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def full_address(self):
        parts = [self.address_line1, self.address_line2, self.city, self.state, self.postal_code, self.country]
        return ', '.join(filter(None, parts))


class CustomerContact(models.Model):
    """Additional contacts for business customers"""
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_contacts'
        verbose_name = 'Customer Contact'
        verbose_name_plural = 'Customer Contacts'
        unique_together = ['customer', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.customer.company_name}"


class CustomerInteraction(models.Model):
    """Track all customer interactions"""
    
    INTERACTION_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('demo', 'Demo'),
        ('support', 'Support Ticket'),
        ('social', 'Social Media'),
        ('website', 'Website Visit'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'customer_interactions'
        verbose_name = 'Customer Interaction'
        verbose_name_plural = 'Customer Interactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.get_interaction_type_display()} - {self.subject}"


class CustomerSegment(models.Model):
    """Customer segmentation for targeted marketing"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    criteria = models.JSONField(default=dict)  # Flexible criteria for segmentation
    customers = models.ManyToManyField(Customer, related_name='segments', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_segments'
        verbose_name = 'Customer Segment'
        verbose_name_plural = 'Customer Segments'
    
    def __str__(self):
        return self.name
    
    @property
    def customer_count(self):
        return self.customers.count()


class CustomerNote(models.Model):
    """Additional notes for customers"""
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_notes'
        verbose_name = 'Customer Note'
        verbose_name_plural = 'Customer Notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"
