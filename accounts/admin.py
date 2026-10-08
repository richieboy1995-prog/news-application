"""Configure the Django admin for user accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Customises the admin interface for users."""

    fieldsets = UserAdmin.fieldsets + (
        (
            "News Application Details",
            {
                "fields": (
                    "role",
                    "publisher",
                    "subscribed_publishers",
                    "subscribed_journalists",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "News Application Details",
            {
                "fields": (
                    "role",
                    "publisher",
                ),
            },
        ),
    )
