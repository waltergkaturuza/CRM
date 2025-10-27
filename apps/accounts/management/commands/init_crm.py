from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile, Permission, RolePermission

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize the CRM system with default data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing CRM system...')
        
        # Create default permissions
        self.create_default_permissions()
        
        # Create default role permissions
        self.create_default_role_permissions()
        
        # Create default admin user if it doesn't exist
        self.create_default_admin()
        
        self.stdout.write(
            self.style.SUCCESS('CRM system initialized successfully!')
        )

    def create_default_permissions(self):
        """Create default permissions for the CRM system"""
        permissions = [
            ('view_customer', 'View Customer', 'customers'),
            ('add_customer', 'Add Customer', 'customers'),
            ('change_customer', 'Change Customer', 'customers'),
            ('delete_customer', 'Delete Customer', 'customers'),
            ('view_lead', 'View Lead', 'leads'),
            ('add_lead', 'Add Lead', 'leads'),
            ('change_lead', 'Change Lead', 'leads'),
            ('delete_lead', 'Delete Lead', 'leads'),
            ('view_deal', 'View Deal', 'deals'),
            ('add_deal', 'Add Deal', 'deals'),
            ('change_deal', 'Change Deal', 'deals'),
            ('delete_deal', 'Delete Deal', 'deals'),
            ('view_analytics', 'View Analytics', 'analytics'),
            ('view_reports', 'View Reports', 'reports'),
            ('manage_users', 'Manage Users', 'accounts'),
            ('manage_settings', 'Manage Settings', 'settings'),
        ]
        
        for codename, name, module in permissions:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                defaults={'name': name, 'module': module}
            )
            if created:
                self.stdout.write(f'Created permission: {name}')

    def create_default_role_permissions(self):
        """Create default role permissions"""
        role_permissions = {
            'admin': [
                'view_customer', 'add_customer', 'change_customer', 'delete_customer',
                'view_lead', 'add_lead', 'change_lead', 'delete_lead',
                'view_deal', 'add_deal', 'change_deal', 'delete_deal',
                'view_analytics', 'view_reports', 'manage_users', 'manage_settings'
            ],
            'manager': [
                'view_customer', 'add_customer', 'change_customer',
                'view_lead', 'add_lead', 'change_lead',
                'view_deal', 'add_deal', 'change_deal',
                'view_analytics', 'view_reports'
            ],
            'sales': [
                'view_customer', 'add_customer', 'change_customer',
                'view_lead', 'add_lead', 'change_lead',
                'view_deal', 'add_deal', 'change_deal',
                'view_analytics'
            ],
            'support': [
                'view_customer', 'change_customer',
                'view_lead', 'change_lead',
                'view_deal'
            ],
            'marketing': [
                'view_customer', 'view_lead', 'add_lead', 'change_lead',
                'view_analytics'
            ],
        }
        
        for role, permission_codenames in role_permissions.items():
            for codename in permission_codenames:
                try:
                    permission = Permission.objects.get(codename=codename)
                    role_permission, created = RolePermission.objects.get_or_create(
                        role=role,
                        permission=permission
                    )
                    if created:
                        self.stdout.write(f'Created role permission: {role} - {permission.name}')
                except Permission.DoesNotExist:
                    self.stdout.write(f'Warning: Permission {codename} not found')

    def create_default_admin(self):
        """Create default admin user if it doesn't exist"""
        if not User.objects.filter(email='admin@crm.com').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@crm.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=admin_user,
                timezone='UTC',
                language='en',
                sales_target=0,
                commission_rate=0
            )
            
            self.stdout.write('Created default admin user: admin@crm.com / admin123')
        else:
            self.stdout.write('Default admin user already exists')
