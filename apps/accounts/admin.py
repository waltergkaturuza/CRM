from django.contrib import admin
from .models import User, UserProfile, Team, Permission, RolePermission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'department', 'is_active', 'created_at']
    list_filter = ['role', 'department', 'is_active', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['last_name', 'first_name']
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'avatar')
        }),
        ('Role & Organization', {
            'fields': ('role', 'department', 'manager')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['date_joined', 'created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'timezone', 'language', 'sales_target', 'commission_rate']
    list_filter = ['timezone', 'language']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    raw_id_fields = ['leader']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'module']
    list_filter = ['module']
    search_fields = ['name', 'codename', 'description']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']
    list_filter = ['role']
    search_fields = ['role', 'permission__name']
