"""Configure the accounts application."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configure the accounts Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """Load account signals when the application starts."""
        from . import signals  # noqa: F401
