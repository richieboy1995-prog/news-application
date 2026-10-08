"""Provide forms for the news application."""

from django import forms

from .models import Article, Newsletter, Publisher


class ArticleForm(forms.ModelForm):
    """Provide a form for creating and editing news articles."""

    class Meta:
        """Define the fields used by the article form."""

        model = Article
        fields = [
            "title",
            "content",
            "publisher",
        ]

    def __init__(self, *args, user=None, **kwargs):
        """Provide all publishers as article choices."""
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["publisher"].queryset = (
            Publisher.objects.all().order_by("name")
        )

    def clean(self):
        """Set the article journalist based on the selected publisher."""
        cleaned_data = super().clean()

        publisher = cleaned_data.get("publisher")

        if self.user:
            if publisher:
                self.instance.journalist = None
            else:
                self.instance.journalist = self.user

        return cleaned_data


class PublisherForm(forms.ModelForm):
    """Provide a form for creating and editing publishers."""

    class Meta:
        """Define the fields used by the publisher form."""

        model = Publisher
        fields = [
            "name",
            "description",
        ]


class NewsletterForm(forms.ModelForm):
    """Provide a form for creating and editing newsletters."""

    class Meta:
        """Define the fields used by the newsletter form."""

        model = Newsletter
        fields = [
            "title",
            "description",
            "articles",
        ]
