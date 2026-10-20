"""Define the models used by the news application."""

from django.db import models
from django.core.exceptions import ValidationError


class Publisher(models.Model):
    """Represents a news publisher.

    A publisher has a name and a description and can be associated
    with multiple news articles.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        """Return the publisher name.

        :returns: The name of the publisher.
        :rtype: str

        """
        return self.name


class Article(models.Model):
    """Represent a news article and its publication status.

    An article has an author, content, a creation date and an approval
    status. It must be associated with either a journalist or a publisher,
    but not both.
    """

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
        """Validate the article's journalist and publisher.

        Ensure that an article is associated with exactly one of
        a journalist or a publisher.

        :raises ValidationError: If both relationships are set or
            if neither relationship is set.
        """

        if self.journalist and self.publisher:
            raise ValidationError(
                "An article cannot have both a journalist and a publisher."
            )

        if not self.journalist and not self.publisher:
            raise ValidationError(
                "An article must have either a journalist or a publisher."
            )

    def __str__(self):
        """Return the article title.

        :returns: The title of the article.
        :rtype: str
        """
        return self.title


class Newsletter(models.Model):
    """Represent a curated collection of news articles.

    A newsletter has a title, description, author and
    a collection of articles.
    """

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
        """Return the newsletter title.

        :returns: The title of the newsletter.
        :rtype: str
        """
        return self.title
