from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@crm.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser "admin"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser "admin" already exists')
            )
