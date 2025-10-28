from django.contrib import admin
from .models import AnalyticsDashboard, KPI, KPIMeasurement, CustomerInsight, LeadInsight, DealInsight, SentimentAnalysis, PredictiveModel, Report, ReportExecution


@admin.register(AnalyticsDashboard)
class AnalyticsDashboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'refresh_interval', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'target_value', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(KPIMeasurement)
class KPIMeasurementAdmin(admin.ModelAdmin):
    list_display = ('kpi', 'value', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('kpi__name',)


@admin.register(CustomerInsight)
class CustomerInsightAdmin(admin.ModelAdmin):
    list_display = ('customer', 'insight_type', 'confidence_score', 'created_at')
    list_filter = ('insight_type', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name')


@admin.register(LeadInsight)
class LeadInsightAdmin(admin.ModelAdmin):
    list_display = ('lead', 'insight_type', 'confidence_score', 'created_at')
    list_filter = ('insight_type', 'created_at')
    search_fields = ('lead__first_name', 'lead__last_name')


@admin.register(DealInsight)
class DealInsightAdmin(admin.ModelAdmin):
    list_display = ('deal', 'insight_type', 'confidence_score', 'created_at')
    list_filter = ('insight_type', 'created_at')
    search_fields = ('deal__name',)


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('content', 'sentiment_score', 'sentiment_label', 'created_at')
    list_filter = ('sentiment_label', 'created_at')
    search_fields = ('content',)


@admin.register(PredictiveModel)
class PredictiveModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'accuracy', 'created_at')
    list_filter = ('model_type', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('name', 'description')


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('report__name',)
