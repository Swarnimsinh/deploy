import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates/updates the superuser defined in environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set in environment variables."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' already exists. Syncing password/email..."
            ))
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.save()
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Creating superuser '{username}'..."
            ))
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
