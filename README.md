# The Woodland Chronicle

A Django-based news application that allows readers, journalists, and editors to interact with a shared news platform.

The application allows readers to browse approved articles, subscribe to publishers and independent journalists, and view a personalised news feed.

Journalists can create articles and newsletters, while editors can review and approve submitted articles.

The application uses an ancient woodland newspaper design inspired by old-world fantasy environments.

---

## Features

### User Accounts

- User registration and login.
- User logout.
- Three user roles:
  - Reader
  - Journalist
  - Editor
- Users are automatically assigned to the appropriate Django group based on their role.
- Email addresses must be unique during registration.

### Readers

Readers can:

- View approved articles.
- View newsletters.
- Subscribe to publishers.
- Unsubscribe from publishers.
- Subscribe to independent journalists.
- Unsubscribe from independent journalists.
- View a personalised feed containing articles from their subscriptions.

### Journalists

Journalists can:

- Create articles.
- Edit their own articles.
- Delete their own articles.
- Create newsletters.
- Edit their own newsletters.
- Delete their own newsletters.
- Publish independently or submit articles through a publisher.

Articles created by journalists require editor approval before they become visible to readers.

### Editors

Editors can:

- View articles waiting for approval.
- Approve submitted articles.
- Edit articles.
- Delete articles.

When an article is approved, subscribed readers can receive an email notification.

---

## REST API

The application also provides a REST API using Django REST Framework.

Available endpoints include:

```text
GET     /api/articles/
GET     /api/articles/subscribed/
GET     /api/articles/<id>/
POST    /api/articles/
PUT     /api/articles/<id>/
DELETE  /api/articles/<id>/
```

The API uses token authentication for protected operations.

---

## Technologies Used

- Python 3.14
- Django 6.1.1
- Django REST Framework 3.18.3
- MariaDB
- MySQLclient 2.3.0
- HTML5
- CSS3
- Django templates
- Django sessions
- Django email backend
- Automated Django tests

---

# Installation and Setup

This section explains how to download, install, configure, and run The Woodland Chronicle on a Windows computer.

The instructions are written for someone setting up the project for the first time.

---

## Before You Begin

Make sure the following software is installed on your computer:

- Python 3.14 or later.
- Git.
- MariaDB.
- Visual Studio Code or another code editor.
- Windows PowerShell.

You can check whether Python is installed by opening PowerShell and entering:

```powershell
python --version
```

You should see a Python version displayed, for example:

```text
Python 3.14.4
```

You can check whether Git is installed with:

```powershell
git --version
```

MariaDB should also be installed and running before continuing.

If any required software is missing, install it before continuing.

---

## Step 1 — Open PowerShell

Open **Windows PowerShell**.

All commands in the installation instructions below should be entered into PowerShell.

---

## Step 2 — Clone the Project

Choose the folder where you want to store the project.

For example, to move to your Desktop:

```powershell
cd Desktop
```

Clone the project from GitHub:

```powershell
git clone https://github.com/richieboy1995-prog/news-application.git
```

Git will download a copy of the project onto your computer.

You should see a new project folder created.

---

## Step 3 — Enter the Project Folder

Move into the downloaded project folder:

```powershell
cd news-application
```

You can check that you are in the correct folder by running:

```powershell
dir
```

You should see files and folders including:

```text
accounts
news
news_application
static
templates
manage.py
requirements.txt
README.md
```

The file `manage.py` is important because it is used to run Django management commands.

---

## Step 4 — Create a Virtual Environment

A virtual environment keeps this project's Python packages separate from other Python projects on your computer.

Make sure you are in the same folder as `manage.py`.

Run:

```