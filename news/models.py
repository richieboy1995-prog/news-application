from django.db import models
from django.core.exceptions import ValidationError


class Publisher(models.Model):
    """Represent a news publisher."""
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Article(models.Model):
    """Represent a news article and its publication status."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="authored_articles",
    )
    journalist = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="independent_articles",
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def clean(self):
        if self.journalist and self.publisher:
            raise ValidationError(
                "An article cannot have both a journalist and a publisher."
            )

        if not self.journalist and not self.publisher:
            raise ValidationError(
                "An article must have either a journalist or a publisher."
            )

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Represent a curated collection of news articles."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="newsletter",
    )
    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
    )

    def __str__(self):
        return self.title
