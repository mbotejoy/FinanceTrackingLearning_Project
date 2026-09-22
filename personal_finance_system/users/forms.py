from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User

# This ensures that the first and last names only contain valid characters.
name_validator = RegexValidator(
    regex=r"^[A-Za-z\s'-]+$",
    message="Name can only contain letters, spaces, hyphens, and apostrophes."
)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, validators=[name_validator])
    last_name = forms.CharField(max_length=150, required=True, validators=[name_validator])
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]