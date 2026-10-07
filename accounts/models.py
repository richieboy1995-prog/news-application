from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Represent a user and their role within the news application."""
    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
    )

    publisher = models.ForeignKey(
        "news.Publisher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    subscribed_publishers = models.ManyToManyField(
        "news.Publisher",
        blank=True,
        related_name="subscribers",
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="reader_subscribers",
    )
