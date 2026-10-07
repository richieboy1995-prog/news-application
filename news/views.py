from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import User

from .serializers import ArticleSerializer
from .forms import ArticleForm, NewsletterForm
from .models import Article, Newsletter, Publisher


def article_list(request):
    articles = Article.objects.filter(approved=True)

    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


@login_required
def create_article(request):
    """Allow a journalist to create an article."""
    if request.user.role != "journalist":
        return redirect("article_list")

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            article = form.save(commit=False)

            article.author = request.user
            article.approved = False

            if article.publisher:
                article.journalist = None
            else:
                article.journalist = request.user

            article.save()

            return redirect("article_list")

    else:
        form = ArticleForm(
            user=request.user,
        )

    return render(
        request,
        "news/create_article.html",
        {"form": form},
    )


@login_required
def pending_articles(request):
    """Display articles waiting for editor approval."""

    if request.user.role != "editor":
        return redirect("article_list")

    articles = Article.objects.filter(
        approved=False
    ).order_by("-created_at")

    return render(
        request,
        "news/pending_articles.html",
        {"articles": articles},
    )


@require_POST
@login_required
def approve_article(request, article_id):
    """Approve an article and notify subscribed readers."""
    if request.user.role != "editor":
        return redirect("article_list")

    article = get_object_or_404(
        Article,
        pk=article_id,
    )

    article.approved = True
    article.save()

    recipients = set()

    if article.publisher:
        publisher_readers = User.objects.filter(
            subscribed_publishers=article.publisher,
        )

        for reader in publisher_readers:
            if reader.email:
                recipients.add(reader.email)

    if article.journalist:
        journalist_readers = User.objects.filter(
            subscribed_journalists=article.journalist,
        )

        for reader in journalist_readers:
            if reader.email:
                recipients.add(reader.email)

    if recipients:
        send_mail(
            subject=f"New article: {article.title}",
            message=(
                f"A new article has been approved.\n\n"
                f"Title: {article.title}\n\n"
                f"{article.content}"
            ),
            from_email=None,
            recipient_list=list(recipients),
        )

    return redirect("pending_articles")


@login_required
def publisher_list(request):
    """Display all available publishers."""
    publishers = Publisher.objects.all().order_by("name")

    return render(
        request,
        "news/publisher_list.html",
        {"publishers": publishers},
    )


@require_POST
@login_required
def subscribe_publisher(request, publisher_id):
    """Subscribe a reader to a publisher."""
    if request.user.role != ("reader"):
        return redirect("publisher_list")

    publisher = get_object_or_404(
        Publisher,
        pk=publisher_id
    )

    request.user.subscribed_publishers.add(publisher)

    return redirect("publisher_list")


@require_POST
@login_required
def unsubscribe_publisher(request, publisher_id):
    """Remove a reader's subscription to a publisher."""
    if request.user.role != "reader":
        return redirect("publisher_list")

    publisher = get_object_or_404(
        Publisher,
        pk=publisher_id,
    )

    request.user.subscribed_publishers.remove(publisher)

    return redirect("publisher_list")


@login_required
def journalist_list(request):
    """Display all independent journalists."""
    journalists = User.objects.filter(
        role="journalist"
    ).order_by("username")

    return render(
        request,
        "news/journalist_list.html",
        {"journalists": journalists},
    )


@require_POST
@login_required
def subscribe_journalist(request, journalist_id):
    """Subscribe a reader to a journalist."""
    if request.user.role != "reader":
        return redirect("journalist_list")

    journalist = get_object_or_404(
        User,
        pk=journalist_id,
        role="journalist",
    )

    request.user.subscribed_journalists.add(journalist)

    return redirect("journalist_list")


@require_POST
@login_required
def unsubscribe_journalist(request, journalist_id):
    """Remove a reader's subscription to a journalist."""
    if request.user.role != "reader":
        return redirect("journalist_list")

    journalist = get_object_or_404(
        User,
        pk=journalist_id,
        role="journalist",
    )

    request.user.subscribed_journalists.remove(journalist)

    return redirect("journalist_list")


@login_required
def subscribed_articles(request):
    """Display approved articles from reader subscriptions."""
    if request.user.role != "reader":
        return redirect("article_list")

    publisher_articles = Article.objects.filter(
        publisher__in=request.user.subscribed_publishers.all(),
        approved=True,
    )

    journalist_articles = Article.objects.filter(
        journalist__in=request.user.subscribed_journalists.all(),
        approved=True,
    )

    articles = (
        publisher_articles | journalist_articles
    ).distinct().order_by("-created_at")

    return render(
        request,
        "news/subscribed_articles.html",
        {"articles": articles},
    )


@login_required
def create_newsletter(request):
    """Allow a journalist to create a newsletter."""
    if request.user.role != "journalist":
        return redirect("article_list")

    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()

            return redirect("newsletter_list")

    else:
        form = NewsletterForm()

    return render(
        request,
        "news/create_newsletter.html",
        {"form": form},
    )


def newsletter_list(request):
    """Display all newsletters."""
    newsletters = Newsletter.objects.all().order_by("-created_at")

    return render(
        request,
        "news/newsletter_list.html",
        {"newsletters": newsletters},
    )


def newsletter_detail(request, newsletter_id):
    """Display the details of a newsletter."""
    newsletter = get_object_or_404(
        Newsletter,
        pk=newsletter_id,
    )

    return render(
        request,
        "news/newsletter_detail.html",
        {"newsletter": newsletter},
    )


@login_required
def edit_article(request, article_id):
    """Allow an authorised user to edit an article."""
    article = get_object_or_404(
        Article,
        pk=article_id,
    )

    if request.user.role not in ["journalist", "editor"]:
        return redirect("article_list")

    if (
        request.user.role == "journalist"
        and article.author != request.user
    ):
        return redirect("article_list")

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            instance=article,
            user=request.user,
        )

        if form.is_valid():
            article = form.save(commit=False)
            article.save()

            return redirect("article_list")

    else:
        form = ArticleForm(
            instance=article,
            user=request.user,
        )

    return render(
        request,
        "news/edit_article.html",
        {"form": form, "article": article},
    )


@login_required
def delete_article(request, article_id):
    """Allow an authorized user to delete an article."""
    article = get_object_or_404(
        Article,
        pk=article_id,
    )

    if request.user.role not in ["journalist", "editor"]:
        return redirect("article_list")

    if (
        request.user.role == "journalist"
        and article.author != request.user
    ):
        return redirect("article_list")

    if request.method == "POST":
        article.delete()

        return redirect("article_list")

    return render(
        request,
        "news/delete_article.html",
        {"article": article},
    )


@login_required
def edit_newsletter(request, newsletter_id):
    """Allow an authorised user to edit a newsletter."""
    newsletter = get_object_or_404(
        Newsletter,
        pk=newsletter_id,
    )

    if request.user.role not in ["journalist", "editor"]:
        return redirect("newsletter_list")

    if (
        request.user.role == "journalist"
        and newsletter.author != request.user
    ):
        return redirect("newsletter_list")

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "newsletter_detail",
                newsletter_id=newsletter.id,
            )

    else:
        form = NewsletterForm(
            instance=newsletter,
        )

    return render(
        request,
        "news/edit_newsletter.html",
        {
            "form": form,
            "newsletter": newsletter,
        },
    )


@login_required
def delete_newsletter(request, newsletter_id):
    """Allow an authorised user to delete a newsletter."""
    newsletter = get_object_or_404(
        Newsletter,
        pk=newsletter_id,
    )

    if request.user.role not in ["journalist", "editor"]:
        return redirect("newsletter_list")

    if (
        request.user.role == "journalist"
        and newsletter.author != request.user
    ):
        return redirect("newsletter_list")

    if request.method == "POST":
        newsletter.delete()

        return redirect("newsletter_list")

    return render(
        request,
        "news/delete_newsletter.html",
        {"newsletter": newsletter},
    )


@api_view(["GET", "POST"])
def api_article_list(request):
    """List approved articles or create an article through the API."""
    if request.method == "GET":
        articles = Article.objects.filter(
            approved=True
        ).order_by("-created_at")

        serializer = ArticleSerializer(
            articles,
            many=True,
        )

        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=401,
        )

    if request.user.role != "journalist":
        return Response(
            {"error": "Only journalists can create articles."},
            status=403,
        )

    serializer = ArticleSerializer(
        data=request.data,
    )

    if serializer.is_valid():
        article = serializer.save(
            author=request.user,
            journalist=request.user,
            approved=False,
        )

        return Response(
            ArticleSerializer(article).data,
            status=201,
        )

    return Response(
        serializer.errors,
        status=400,
    )


@api_view(["GET"])
def api_subscribed_articles(request):
    """Return approved articles from a reader's subscriptions."""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=401,
        )

    if request.user.role != "reader":
        return Response(
            {"error": "Only readers can view subscribed articles."},
            status=403,
        )

    publisher_articles = Article.objects.filter(
        publisher__in=request.user.subscribed_publishers.all(),
        approved=True,
    )

    journalist_articles = Article.objects.filter(
        journalist__in=request.user.subscribed_journalists.all(),
        approved=True,
    )

    articles = (
        publisher_articles | journalist_articles
    ).distinct().order_by("-created_at")

    serializer = ArticleSerializer(
        articles,
        many=True,
    )

    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def api_article_detail(request, article_id):
    """Retrieve, update, or delete an individual article through the API."""
    article = get_object_or_404(
        Article,
        pk=article_id,
    )

    if request.method == "GET":
        if not article.approved:
            return Response(
                {"error": "Article is not approved."},
                status=404,
            )

        serializer = ArticleSerializer(article)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=401,
        )

    if request.user.role not in ["journalist", "editor"]:
        return Response(
            {
                "error": (
                    "Only journalists and editors can update "
                    "or delete articles."
                )
            },
            status=403,
        )

    if (
        request.user.role == "journalist"
        and article.author != request.user
    ):
        return Response(
            {"error": "You can only modify your own articles."},
            status=403,
        )

    if request.method == "PUT":
        serializer = ArticleSerializer(
            article,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            article = serializer.save()

            return Response(
                ArticleSerializer(article).data,
                status=200,
            )

        return Response(
            serializer.errors,
            status=400,
        )

    if request.method == "DELETE":
        article.delete()

        return Response(status=204)
