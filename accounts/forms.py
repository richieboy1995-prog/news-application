"""Provide forms for user registration."""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """Provide registration and email validation for new users."""

    email = forms.EmailField(
        required=True,
    )

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
    )

    class Meta:
        """Define the fields used by the registration form."""

        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "role",
        ]

    def clean_email(self):
        """Validate that the email address is not already registered."""
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email
