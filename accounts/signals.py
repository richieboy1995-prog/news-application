"""Define signals for user role group assignment."""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_role_group(sender, instance, **kwargs):
    """Assign the user to the group matching their selected role."""
    if not instance.role:
        return

    group_name = instance.role.capitalize()

    group = Group.objects.filter(
        name=group_name
    ).first()

    if not group:
        return

    if not instance.groups.filter(
        name=group_name
    ).exists():
        instance.groups.clear()
        instance.groups.add(group)
