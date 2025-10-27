from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom User model with additional CRM-specific fields"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('sales', 'Sales Representative'),
        ('support', 'Support Agent'),
        ('marketing', 'Marketing Specialist'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales')
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES)[self.role]


class UserProfile(models.Model):
    """Extended user profile with CRM-specific settings"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    notification_preferences = models.JSONField(default=dict)
    dashboard_settings = models.JSONField(default=dict)
    sales_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.full_name} Profile"


class Team(models.Model):
    """Teams for organizing users"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        return self.members.count()


class Permission(models.Model):
    """Custom permissions for CRM features"""
    
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)  # e.g., 'customers', 'deals', 'analytics'
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
    
    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """Many-to-many relationship between roles and permissions"""
    
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
    
    def __str__(self):
        return f"{self.get_role_display()} - {self.permission.name}"
