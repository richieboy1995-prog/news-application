from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
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
