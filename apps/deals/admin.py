from django.contrib import admin
from .models import Deal, DealActivity, DealProduct, DealStage, SalesPipeline, DealForecast


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'stage', 'value', 'probability', 'expected_close_date', 'assigned_to')
    list_filter = ('stage', 'probability', 'expected_close_date', 'created_at')
    search_fields = ('name', 'customer__first_name', 'customer__last_name', 'customer__company_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DealActivity)
class DealActivityAdmin(admin.ModelAdmin):
    list_display = ('deal', 'activity_type', 'user', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('deal__name', 'notes')


@admin.register(DealProduct)
class DealProductAdmin(admin.ModelAdmin):
    list_display = ('deal', 'name', 'quantity', 'unit_price', 'total_price')
    search_fields = ('deal__name', 'name')


@admin.register(DealStage)
class DealStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'probability')
    search_fields = ('name', 'description')
    ordering = ('order',)


@admin.register(SalesPipeline)
class SalesPipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(DealForecast)
class DealForecastAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
    list_filter = ('created_at',)
    search_fields = ()