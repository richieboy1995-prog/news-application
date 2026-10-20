"""Provide views for user registration and authentication."""

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    """Register a new user and log them into the application.

    Process the registration form and redirect to the article list
    when registration succeeds.

    :param request: The HTTP request received from the browser.
    :type request: HttpRequest
    :returns: The registration page or a redirect to the article list.
    :rtype: HttpResponse
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("article_list")
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def logout_view(request):
    """Log the current user out of the application.

    Redirect to the article list after logging out.

    :param request: The HTTP request received from the browser
    :type request: HttpRequest
    :returns: A redirect to the article list.
    :rtype: HttpResponse
    """
    logout(request)

    return redirect("article_list")


def login_view(request):
    """Authenticate a user and log them into the application.

    Process the login form and redirect to the article list
    when authentication succeeds.

    :param request: The HTTP request received from the browser
    :type request: HttpRequest
    :returns: The login page or a redirect to the article list
    :rtype: HttpResponse
    """
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("article_list")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )
