# The Woodland Chronicle

A Django-based news application that allows readers, journalists, and editors to interact with a shared news platform.

The application allows readers to browse approved articles, subscribe to publishers and independent journalists, and view a personalised news feed.

Journalists can create articles and newsletters, while editors can review and approve submitted articles.

I also wanted to add a more of an Lord of the rings feel to the site.

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
GET    /api/articles/
GET    /api/articles/subscribed/
GET    /api/articles/<id>/
POST   /api/articles/
PUT    /api/articles/<id>/
DELETE /api/articles/<id>/
```

The API uses token authentication for protected operations.

---

## Technologies Used

- Python 3.14
- Django 6.1.1
- Django REST Framework
- SQLite
- HTML5
- CSS3
- Django templates
- Django sessions
- Django email backend
- Automated Django tests

---

# Installation and Setup

This section explains how to download, install, and run the Woodland Chronicle on a Windows computer.

The instructions are written for someone who is setting up the project for the first time.

---

## Before You Begin

Make sure the following software is installed on your computer:

- Python 3.14 or later.
- Git.
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

You should see a Git version displayed.

If either command is not recognised, install the missing software before continuing.

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

```powershell
python -m venv venv
```

This creates a folder called:

```text
venv
```

The virtual environment does not need to be uploaded to GitHub.

---

## Step 5 — Activate the Virtual Environment

Activate the virtual environment using:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation was successful, PowerShell should show:

```text
(venv)
```

at the beginning of the command prompt.

For example:

```text
(venv) PS C:\Users\YourName\Desktop\news-application>
```

If PowerShell does not allow the activation script to run, enter:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try the activation command again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Step 6 — Install the Required Python Packages

Make sure the virtual environment is activated.

Install all packages required by the project:

```powershell
pip install -r requirements.txt
```

This reads the `requirements.txt` file and installs the required Python packages.

Wait for the installation to finish before continuing.

---

## Step 7 — Check the Django Project

Before setting up the database, check

# Using the Application

## Registering an Account

Open the registration page:

```text
/register/
```

Enter:

- Username
- Email address
- Password
- User role

The available roles are:

- Reader
- Journalist
- Editor

After registration, the user is automatically logged in.

---

## Reader Workflow

A reader can:

1. Log in.
2. Browse approved articles.
3. Open the Publishers page.
4. Subscribe to a publisher.
5. Open the Journalists page.
6. Subscribe to an independent journalist.
7. Open My Feed.
8. View articles from their subscriptions.
9. Browse newsletters.

---

## Journalist Workflow

A journalist can:

1. Log in.
2. Select **Write Article**.
3. Enter the article information.
4. Submit the article.
5. Wait for editor approval.
6. Edit or delete their own articles.
7. Create newsletters.
8. Select articles for the newsletter.
9. Edit or delete their own newsletters.

Articles are not immediately displayed to readers because they require approval.

---

## Editor Workflow

An editor can:

1. Log in.
2. Open **Pending Articles**.
3. Review submitted articles.
4. Approve an article.
5. The article then becomes available to readers.
6. An email notification can be sent to readers subscribed to the relevant publisher or journalist.

Editors can also edit and delete articles.

---

# Running the Tests

The project includes automated tests for important application functionality.

Run the tests with:

```powershell
python manage.py test news
```

The tests cover functionality including:

- Article API access.
- Article creation.
- Article updates.
- Article deletion.
- Reader permissions.
- Journalist permissions.
- Editor permissions.
- Subscribed article feeds.
- Newsletter creation.
- Newsletter editing.
- Newsletter deletion.
- Article approval.
- Approval email behaviour.

---

# Project Structure

```text
news_application/
│
├── accounts/
│   ├── migrations/
│   ├── management/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
│
├── news/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── news_application/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── base.html
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Important Notes

The `venv` directory is not included in the Git repository.

The local SQLite database is also excluded from Git using `.gitignore`.

After cloning the project, the database can be recreated by running:

```powershell
python manage.py migrate
```

The project uses Django's development email backend for testing approval notifications. Emails are displayed in the terminal rather than being sent to real email addresses.

---

# Design

The application uses an ancient woodland newspaper theme inspired by old-world fantasy environments.

The design includes:

- Forest green navigation.
- Warm parchment-style article cards.
- Brown and gold accents.
- Responsive layouts.
- Decorative woodland dividers.
- A shared navigation and footer.
- Consistent styling across the application's pages.

The design is intended to give the application the appearance of an old woodland newspaper while remaining suitable for a modern news application.