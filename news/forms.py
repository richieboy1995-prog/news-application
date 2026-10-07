from django import forms

from .models import Article, Newsletter, Publisher


class ArticleForm(forms.ModelForm):
    """Provide a form for creating and editing news articles."""

    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "publisher",
        ]

    def __init__(self, *args, user=None, **kwargs):
        """Limit publisher choices to the user's publisher."""
        super().__init__(*args, **kwargs)

        self.user = user

        if user and user.publisher:
            self.fields["publisher"].queryset = Publisher.objects.filter(
                pk=user.publisher.pk
            )
        else:
            self.fields["publisher"].queryset = Publisher.objects.none()

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


class NewsletterForm(forms.ModelForm):
    """Provide a form for creating and editing newsletters."""

    class Meta:
        model = Newsletter
        fields = [
            "title",
            "description",
            "articles",
        ]
