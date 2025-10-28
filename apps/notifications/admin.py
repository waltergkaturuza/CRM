from django.contrib import admin
from .models import NotificationTemplate, NotificationPreference, NotificationQueue, NotificationDelivery, NotificationCampaign, NotificationSubscription


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'subject', 'content')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(NotificationQueue)
class NotificationQueueAdmin(admin.ModelAdmin):
    list_display = ('template', 'recipient', 'status', 'scheduled_at', 'created_at')
    list_filter = ('status', 'scheduled_at', 'created_at')
    search_fields = ('template__name', 'recipient__username')


@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ('status', 'delivered_at', 'created_at')
    list_filter = ('status', 'delivered_at', 'created_at')
    search_fields = ()


@admin.register(NotificationCampaign)
class NotificationCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
