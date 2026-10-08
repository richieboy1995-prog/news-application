"""Define tests for the news application."""

from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from accounts.models import User
from .models import Article, Newsletter, Publisher


class ArticleAPITest(TestCase):
    """Test the article REST API endpoints."""

    def setUp(self):
        """Set up users, a publisher, and test articles."""
        self.client = APIClient()

        self.journalist = User.objects.create_user(
            username="testjournalist",
            password="TestPass123!",
            email="journalist@example.com",
            role="journalist",
        )

        self.second_journalist = User.objects.create_user(
            username="secondjournalist",
            password="TestPass123!",
            email="second@example.com",
            role="journalist",
        )

        self.reader = User.objects.create_user(
            username="testreader",
            password="TestPass123!",
            email="reader@example.com",
            role="reader",
        )

        self.editor = User.objects.create_user(
            username="testeditor",
            password="TestPass123!",
            email="editor@example.com",
            role="editor",
        )

        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            description="Publisher used for automated testing.",
        )

        self.journalist.publisher = self.publisher
        self.journalist.save()

        self.approved_article = Article.objects.create(
            title="Approved Test Article",
            content="This article should appear in the API.",
            author=self.journalist,
            journalist=self.journalist,
            approved=True,
        )

        self.unapproved_article = Article.objects.create(
            title="Unapproved Test Article",
            content="This article should not appear in the API.",
            author=self.journalist,
            journalist=self.journalist,
            approved=False,
        )

    def test_get_articles_returns_approved_articles(self):
        """Test that the API returns approved articles only."""
        response = self.client.get("/api/articles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Approved Test Article",
        )

    def test_journalist_can_create_article(self):
        """Test that a journalist can create an article through the API."""
        self.client.force_authenticate(user=self.journalist)

        data = {
            "title": "Created Through API",
            "content": "This article was created by an automated test.",
        }

        response = self.client.post(
            "/api/articles/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["title"],
            "Created Through API",
        )
        self.assertEqual(
            response.data["author"],
            self.journalist.id,
        )

    def test_reader_cannot_create_article(self):
        """Test that a reader cannot create an article."""
        self.client.force_authenticate(user=self.reader)

        data = {
            "title": "Reader Article",
            "content": "A reader should not be able to create this.",
        }

        response = self.client.post(
            "/api/articles/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_create_article(self):
        """Test that unauthenticated users cannot create articles."""
        data = {
            "title": "Unauthorised Article",
            "content": "This should not be created.",
        }

        response = self.client.post(
            "/api/articles/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_reader_only_receives_subscribed_articles(self):
        """Test that readers only receive articles from subscriptions."""
        self.reader.subscribed_journalists.add(
            self.journalist
        )

        self.client.force_authenticate(user=self.reader)

        response = self.client.get(
            "/api/articles/subscribed/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Approved Test Article",
        )

    def test_get_approved_article_detail(self):
        """Test that an approved article can be retrieved individually."""
        response = self.client.get(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Approved Test Article",
        )

    def test_unapproved_article_detail_returns_404(self):
        """Test that an unapproved article cannot be retrieved."""
        response = self.client.get(
            f"/api/articles/{self.unapproved_article.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_journalist_can_update_own_article(self):
        """Test that a journalist can update their own article."""
        self.client.force_authenticate(
            user=self.journalist
        )

        data = {
            "title": "Updated Article",
            "content": "Updated content.",
        }

        response = self.client.put(
            f"/api/articles/{self.approved_article.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Updated Article",
        )

    def test_journalist_cannot_update_another_journalists_article(
        self,
    ):
        """Test that a journalist cannot update another journalist."""
        self.client.force_authenticate(
            user=self.second_journalist
        )

        data = {
            "title": "Unauthorised Update",
            "content": "This should not be allowed.",
        }

        response = self.client.put(
            f"/api/articles/{self.approved_article.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_editor_can_update_article(self):
        """Test that an editor can update an article."""
        self.client.force_authenticate(
            user=self.editor
        )

        data = {
            "title": "Editor Updated Article",
            "content": "Updated by the editor.",
        }

        response = self.client.put(
            f"/api/articles/{self.approved_article.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Editor Updated Article",
        )

    def test_journalist_can_delete_own_article(self):
        """Test that a journalist can delete their own article."""
        self.client.force_authenticate(
            user=self.journalist
        )

        response = self.client.delete(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Article.objects.filter(
                id=self.approved_article.id
            ).exists()
        )

    def test_journalist_cannot_delete_another_journalists_article(
        self,
    ):
        """Test that a journalist cannot delete another journalist."""
        self.client.force_authenticate(
            user=self.second_journalist
        )

        response = self.client.delete(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_delete_article(self):
        """Test that a reader cannot delete an article."""
        self.client.force_authenticate(
            user=self.reader
        )

        response = self.client.delete(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 403)


class NewsletterTest(TestCase):
    """Test newsletter creation, editing, and deletion."""

    def setUp(self):
        """Set up the users and article used by newsletter tests."""
        self.client = APIClient()

        self.journalist = User.objects.create_user(
            username="newsletterjournalist",
            password="TestPass123!",
            email="newsletter@example.com",
            role="journalist",
        )

        self.reader = User.objects.create_user(
            username="newsletterreader",
            password="TestPass123!",
            email="reader@example.com",
            role="reader",
        )

        self.article = Article.objects.create(
            title="Newsletter Article",
            content="Article used in newsletter testing.",
            author=self.journalist,
            journalist=self.journalist,
            approved=True,
        )

    def test_journalist_can_create_newsletter(self):
        """Test that a journalist can create a newsletter."""
        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse("create_newsletter"),
            {
                "title": "Test Newsletter",
                "description": "A newsletter created by a test.",
                "articles": [self.article.id],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Newsletter.objects.filter(
                title="Test Newsletter"
            ).exists()
        )

    def test_journalist_can_edit_newsletter(self):
        """Test that a journalist can edit their own newsletter."""
        newsletter = Newsletter.objects.create(
            title="Original Newsletter",
            description="Original description.",
            author=self.journalist,
        )

        newsletter.articles.add(self.article)

        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse(
                "edit_newsletter",
                args=[newsletter.id],
            ),
            {
                "title": "Updated Newsletter",
                "description": "Updated description.",
                "articles": [self.article.id],
            },
        )

        self.assertEqual(response.status_code, 302)

        newsletter.refresh_from_db()

        self.assertEqual(
            newsletter.title,
            "Updated Newsletter",
        )

    def test_journalist_can_delete_newsletter(self):
        """Test that a journalist can delete their own newsletter."""
        newsletter = Newsletter.objects.create(
            title="Delete Newsletter",
            description="Newsletter to delete.",
            author=self.journalist,
        )

        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse(
                "delete_newsletter",
                args=[newsletter.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Newsletter.objects.filter(
                id=newsletter.id
            ).exists()
        )


class ArticleApprovalTest(TestCase):
    """Test article approval and subscriber email notification."""

    def setUp(self):
        """Set up users and an article waiting for approval."""
        self.client = APIClient()

        self.editor = User.objects.create_user(
            username="approvaleditor",
            password="TestPass123!",
            email="editor@example.com",
            role="editor",
        )

        self.journalist = User.objects.create_user(
            username="approvaljournalist",
            password="TestPass123!",
            email="journalist@example.com",
            role="journalist",
        )

        self.reader = User.objects.create_user(
            username="approvalreader",
            password="TestPass123!",
            email="reader@example.com",
            role="reader",
        )

        self.article = Article.objects.create(
            title="Article Waiting for Approval",
            content="This article needs editor approval.",
            author=self.journalist,
            journalist=self.journalist,
            approved=False,
        )

        self.reader.subscribed_journalists.add(
            self.journalist
        )

    def test_editor_can_approve_article_and_send_email(self):
        """Test that approval publishes an article.

        and sends notification email.
        """
        self.client.force_login(self.editor)

        with patch("news.views.send_mail") as mock_send_mail:
            response = self.client.post(
                reverse(
                    "approve_article",
                    args=[self.article.id],
                )
            )

        self.assertEqual(response.status_code, 302)

        self.article.refresh_from_db()

        self.assertTrue(self.article.approved)

        mock_send_mail.assert_called_once()

        email_call = mock_send_mail.call_args

        self.assertEqual(
            email_call.kwargs["subject"],
            "New article: Article Waiting for Approval",
        )

        self.assertIn(
            "reader@example.com",
            email_call.kwargs["recipient_list"],
        )
