"""Create groups and permissions for user roles."""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create user role groups and assign model permissions."""

    help = "Create user role groups and assign permissions."

    def handle(self, *args, **options):
        """Create groups and assign their required permissions."""
        groups = {
            "Reader": [
                ("article", "view_article"),
                ("newsletter", "view_newsletter"),
            ],
            "Journalist": [
                ("article", "add_article"),
                ("article", "view_article"),
                ("article", "change_article"),
                ("article", "delete_article"),
                ("newsletter", "add_newsletter"),
                ("newsletter", "view_newsletter"),
                ("newsletter", "change_newsletter"),
                ("newsletter", "delete_newsletter"),
            ],
            "Editor": [
                ("article", "view_article"),
                ("article", "change_article"),
                ("article", "delete_article"),
                ("newsletter", "view_newsletter"),
                ("newsletter", "change_newsletter"),
                ("newsletter", "delete_newsletter"),
            ],
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(
                name=group_name
            )

            for model_name, permission_code in permissions:
                permission = Permission.objects.filter(
                    codename=permission_code,
                    content_type__model=model_name,
                ).first()

                if permission:
                    group.permissions.add(permission)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {group_name} group."
                    )
                )
            else:
                self.stdout.write(
                    f"{group_name} group already exists."
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Groups and permissions configured successfully."
            )
        )
