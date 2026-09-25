from email.policy import default

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom user model extending Django's built-in auth user
class User(AbstractUser):
    ROLE_CHOICES = [
        ("student" , "Student"),
        ("admin", "Admin"),
    ]

    # Email used as the unique login identifier instead of username
    email = models.EmailField(
        unique=True,
    )

    role = models.CharField(
        max_length = 20,
        choices = ROLE_CHOICES,
        default="student"
    )

    # Log in with email, but username is still required on creation
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


