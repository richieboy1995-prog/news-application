"""Define serializers for the news application's REST API."""

from rest_framework import serializers

from accounts.models import User

from .models import Article, Newsletter, Publisher
from django.core.exceptions import ValidationError


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

    def create(self, validated_data):
        """Create an article with valid author relationships."""
        request = self.context.get("request")
        publisher = validated_data.get("publisher")

        if publisher:
            validated_data["journalist"] = None
        elif request and request.user.is_authenticated:
            validated_data["journalist"] = request.user

        article = Article(**validated_data)

        try:
            article.full_clean()
        except ValidationError as error:
            raise serializers.ValidationError(
                error.message_dict
            )

        article.save()
        return article


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
