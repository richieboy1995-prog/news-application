"""Define serializers for the news application's REST API."""

from rest_framework import serializers

from accounts.models import User

from .models import Article, Newsletter, Publisher


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize article data for the REST API."""

    class Meta:
        """Define the fields used by the article serializer."""

        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "journalist",
            "publisher",
            "created_at",
            "approved",
        ]
        read_only_fields = [
            "id",
            "author",
            "journalist",
            "created_at",
            "approved",
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serialize user information for the REST API."""

    class Meta:
        """Define the fields used by the user serializer."""

        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """Serialize newsletter data for the REST API."""

    class Meta:
        """Define the fields used by the newsletter serializer."""

        model = Newsletter
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "author",
            "articles",
        ]


class PublisherSerializer(serializers.ModelSerializer):
    """Serialize publisher information for the REST API."""

    class Meta:
        """Define the fields used by the publisher serializer."""

        model = Publisher
        fields = [
            "id",
            "name",
            "description",
        ]
