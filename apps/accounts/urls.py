from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, TeamViewSet,
    PermissionViewSet, RolePermissionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'role-permissions', RolePermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
