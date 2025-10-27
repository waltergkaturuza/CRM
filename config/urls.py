from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/leads/', include('apps.leads.urls')),
    path('api/deals/', include('apps.deals.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/automation/', include('apps.automation.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
