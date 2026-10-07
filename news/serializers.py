from rest_framework import serializers

from accounts.models import User

from .models import Article, Newsletter, Publisher


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize article data for the REST API."""

    class Meta:
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
        model = Publisher
        fields = [
            "id",
            "name",
            "description",
        ]
