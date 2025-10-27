from django.db import models
from apps.accounts.models import User
from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.deals.models import Deal


class AnalyticsDashboard(models.Model):
    """User-specific analytics dashboard configurations"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics_dashboard')
    widgets = models.JSONField(default=list)  # Dashboard widget configuration
    filters = models.JSONField(default=dict)  # Default filters
    refresh_interval = models.PositiveIntegerField(default=300)  # seconds
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_dashboards'
        verbose_name = 'Analytics Dashboard'
        verbose_name_plural = 'Analytics Dashboards'
    
    def __str__(self):
        return f"{self.user.full_name} Dashboard"


class KPI(models.Model):
    """Key Performance Indicators"""
    
    KPI_TYPE_CHOICES = [
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('customer', 'Customer'),
        ('financial', 'Financial'),
        ('operational', 'Operational'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    kpi_type = models.CharField(max_length=20, choices=KPI_TYPE_CHOICES)
    formula = models.TextField()  # SQL or calculation formula
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, default='count')  # count, percentage, currency, etc.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'kpis'
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
    
    def __str__(self):
        return self.name


class KPIMeasurement(models.Model):
    """Historical KPI measurements"""
    
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='measurements')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    metadata = models.JSONField(default=dict)  # Additional context
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'kpi_measurements'
        verbose_name = 'KPI Measurement'
        verbose_name_plural = 'KPI Measurements'
        unique_together = ['kpi', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.kpi.name} - {self.value} ({self.period_start.strftime('%Y-%m-%d')})"


class CustomerInsight(models.Model):
    """AI-generated customer insights"""
    
    INSIGHT_TYPE_CHOICES = [
        ('behavior', 'Behavior Analysis'),
        ('segmentation', 'Segmentation'),
        ('churn_prediction', 'Churn Prediction'),
        ('upsell_opportunity', 'Upsell Opportunity'),
        ('satisfaction', 'Satisfaction Analysis'),
        ('engagement', 'Engagement Analysis'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.PositiveIntegerField(default=0)  # 0-100%
    data_points = models.JSONField(default=dict)  # Supporting data
    recommendations = models.JSONField(default=list)  # AI recommendations
    is_actionable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customer_insights'
        verbose_name = 'Customer Insight'
        verbose_name_plural = 'Customer Insights'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"


class LeadInsight(models.Model):
    """AI-generated lead insights and scoring"""
    
    INSIGHT_TYPE_CHOICES = [
        ('scoring', 'Lead Scoring'),
        ('qualification', 'Qualification Analysis'),
        ('conversion_prediction', 'Conversion Prediction'),
        ('timing', 'Optimal Timing'),
        ('channel_preference', 'Channel Preference'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.PositiveIntegerField(default=0)  # 0-100%
    score_breakdown = models.JSONField(default=dict)  # Detailed scoring factors
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lead_insights'
        verbose_name = 'Lead Insight'
        verbose_name_plural = 'Lead Insights'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lead.full_name} - {self.title}"


class DealInsight(models.Model):
    """AI-generated deal insights and predictions"""
    
    INSIGHT_TYPE_CHOICES = [
        ('win_probability', 'Win Probability'),
        ('close_prediction', 'Close Date Prediction'),
        ('risk_assessment', 'Risk Assessment'),
        ('upsell_opportunity', 'Upsell Opportunity'),
        ('competitor_analysis', 'Competitor Analysis'),
    ]
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.PositiveIntegerField(default=0)  # 0-100%
    predicted_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    predicted_close_date = models.DateTimeField(null=True, blank=True)
    risk_factors = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'deal_insights'
        verbose_name = 'Deal Insight'
        verbose_name_plural = 'Deal Insights'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.deal.name} - {self.title}"


class SentimentAnalysis(models.Model):
    """Sentiment analysis of customer communications"""
    
    SOURCE_CHOICES = [
        ('email', 'Email'),
        ('call', 'Phone Call'),
        ('chat', 'Live Chat'),
        ('survey', 'Survey'),
        ('social', 'Social Media'),
        ('review', 'Review'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sentiment_analyses')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    content = models.TextField()
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2)  # -1.0 to 1.0
    sentiment_label = models.CharField(max_length=20)  # positive, negative, neutral
    confidence = models.PositiveIntegerField(default=0)  # 0-100%
    keywords = models.JSONField(default=list)  # Key terms extracted
    emotions = models.JSONField(default=dict)  # Emotion analysis
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sentiment_analyses'
        verbose_name = 'Sentiment Analysis'
        verbose_name_plural = 'Sentiment Analyses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.sentiment_label} ({self.confidence}%)"


class PredictiveModel(models.Model):
    """AI/ML models for predictions"""
    
    MODEL_TYPE_CHOICES = [
        ('churn_prediction', 'Churn Prediction'),
        ('lead_scoring', 'Lead Scoring'),
        ('deal_forecasting', 'Deal Forecasting'),
        ('upsell_prediction', 'Upsell Prediction'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('customer_lifetime_value', 'Customer Lifetime Value'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    model_type = models.CharField(max_length=30, choices=MODEL_TYPE_CHOICES)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, default='1.0')
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    training_data_size = models.PositiveIntegerField(null=True, blank=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    parameters = models.JSONField(default=dict)  # Model parameters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'predictive_models'
        verbose_name = 'Predictive Model'
        verbose_name_plural = 'Predictive Models'
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class Report(models.Model):
    """Custom reports and analytics"""
    
    REPORT_TYPE_CHOICES = [
        ('sales', 'Sales Report'),
        ('marketing', 'Marketing Report'),
        ('customer', 'Customer Report'),
        ('financial', 'Financial Report'),
        ('custom', 'Custom Report'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    query = models.TextField()  # SQL query or configuration
    parameters = models.JSONField(default=dict)  # Report parameters
    filters = models.JSONField(default=dict)  # Default filters
    is_scheduled = models.BooleanField(default=False)
    schedule_cron = models.CharField(max_length=100, blank=True)  # Cron expression
    recipients = models.JSONField(default=list)  # Email recipients
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
    
    def __str__(self):
        return self.name


class ReportExecution(models.Model):
    """Report execution history"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField(default=dict)
    result_data = models.JSONField(default=dict, null=True, blank=True)
    error_message = models.TextField(blank=True)
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # milliseconds
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'report_executions'
        verbose_name = 'Report Execution'
        verbose_name_plural = 'Report Executions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.report.name} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
