import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates or updates a superuser from environment variables."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING("DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set. Skipping admin creation."))
            return

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.email = email
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            # Update password if it doesn't match? 
            # Ideally we only update if explicitly requested, but for simplicity in this use case,
            # we enforce the env var state.
            if not user.check_password(password):
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' password updated (Env var differed from DB)."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' password unchanged (Env var matches DB)."))
