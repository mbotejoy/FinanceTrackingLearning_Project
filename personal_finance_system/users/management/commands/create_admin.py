
from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q


class Command(BaseCommand):
    help = "Create a FinanceWise administrator account."

    def handle(self, *args, **options):
        User = get_user_model()

        email = input("Admin email: ").strip().lower()

        if not email:
            raise CommandError("Email is required.")

        if User.objects.filter(
            Q(email__iexact=email) | Q(username__iexact=email)
        ).exists():
            raise CommandError("An account with this email already exists.")

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()

        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            raise CommandError("Passwords do not match.")

        candidate = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        try:
            validate_password(password, user=candidate)
        except ValidationError as error:
            raise CommandError(
                "; ".join(error.messages)
            ) from error

        with transaction.atomic():
            admin = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="admin",
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Administrator created successfully: {admin.email}"
            )
        )
