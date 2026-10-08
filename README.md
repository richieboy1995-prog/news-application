# The Woodland Chronicle

The Woodland Chronicle is a Django-based news application designed to provide a simple online newspaper experience. The application allows readers to view and subscribe to articles, journalists to create articles, and editors to manage and approve articles.

The project uses an ancient woodland theme throughout the website, inspired by The Lord of the Rings.

I wanted to give it my own personal touch and make it look like a Lord of the Rings letter.

## Features

### User Accounts

The application supports three different user roles:

- **Readers**
  - Register for an account.
  - Log in and log out.
  - Subscribe to journalists.
  - Subscribe to publishers.
  - View articles from subscribed journalists and publishers.
  - View individual articles.

- **Journalists**
  - Log in using their account.
  - Create articles.
  - Edit their own articles.
  - Delete their own articles.
  - View their submitted articles.
  - Articles written by journalists must be approved by an editor before they are published.

- **Editors**
  - Log in using their account.
  - View pending articles.
  - Approve articles.
  - Manage publishers.
  - Create publishers.
  - Edit publishers.
  - Delete publishers.
  - View articles and users.

### Article Management

Articles contain information such as:

- Title
- Content
- Author
- Journalist
- Publisher
- Creation date
- Approval status

Articles can be associated with either a journalist or a publisher.

Articles submitted by journalists must be approved by an editor before they become available to readers.

### Publisher Management

Editors can manage publishers through the website.

Editors can:

- Create publishers.
- View publishers.
- Edit publishers.
- Delete publishers.

Publishers can also be assigned to articles.

### Newsletter

Readers can subscribe to newsletters and receive updates about new content.

### REST API

The application provides a REST API using Django REST Framework.

Available API endpoints include:

```text
GET     /api/articles/
GET     /api/articles/subscribed/
GET     /api/articles/<id>/
POST    /api/articles/
PUT     /api/articles/<id>/
DELETE  /api/articles/<id>/
POST    /api/token/
POST    /api/approved/
```

The API uses token authentication for protected requests.

The token endpoint can be used to obtain an authentication token:

```text
POST /api/token/
```

The request should contain the user's username and password.

The approval endpoint allows an authenticated editor to approve an article:

```text
POST /api/approved/
```

The request should contain the article ID.

Example:

```json
{
    "article_id": 1
}
```

Only users with the editor role can approve articles.

## Technologies

The project was developed using:

- Python 3.14
- Django 6.1.1
- Django REST Framework 3.18.3
- MariaDB
- MySQLclient
- HTML
- CSS
- Django Templates
- Django Sessions
- Requests
- Flake8
- Flake8-docstrings

## Project Structure

The main project structure is organized as follows:

```text
news_application/
|
|-- accounts/
|   |-- migrations/
|   |-- management/
|   |-- templates/
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   `-- views.py
|
|-- news/
|   |-- migrations/
|   |-- templates/
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- serializers.py
|   |-- urls.py
|   `-- views.py
|
|-- news_application/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|
|-- static/
|
|-- templates/
|
|-- manage.py
|-- requirements.txt
|-- .flake8
|-- .gitignore
`-- README.md

## Installation and Setup

The following instructions are written for someone who has downloaded the project and wants to run it on a Windows computer.

### Before You Begin

Make sure the following software is installed:

- Python 3.14 or later
- Git
- MariaDB
- Visual Studio Code or another code editor
- Windows PowerShell

You can check whether Python and Git are installed by opening PowerShell and running:

```powershell
python --version
```

and:

```powershell
git --version
```

You should also make sure MariaDB is installed and running.

## Step 1: Clone the Repository

Open PowerShell and navigate to the location where you want to store the project.

Clone the GitHub repository:

```powershell
git clone https://github.com/richieboy1995-prog/news-application.git
```

Move into the project folder:

```powershell
cd news-application
```

You can check that you are in the correct folder by running:

```powershell
dir
```

You should see files and folders such as:

```text
manage.py
requirements.txt
accounts
news
news_application
```

## Step 2: Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv venv
```

This creates a separate environment for the Python packages required by the project.

## Step 3: Activate the Virtual Environment

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, `(venv)` should appear at the beginning of the PowerShell command line.

For example:

```text
(venv) PS C:\Users\YourName\news-application>
```

If PowerShell prevents the activation script from running, the execution policy may need to be adjusted.

## Step 4: Install the Required Packages

With the virtual environment activated, install the packages listed in `requirements.txt`:

```powershell
pip install -r requirements.txt
```

This installs the required versions of Django, Django REST Framework, MySQLclient, Flake8, and the other project dependencies.

## Step 5: Create the MariaDB Database

Open the MariaDB command line.

For example:

```powershell
mysql -u root -p
```

Enter your MariaDB password when prompted.

Create the project database:

```sql
CREATE DATABASE news_application;
```

You can then leave the MariaDB command line:

```sql
exit;
```

## Step 6: Configure the Database

Open the project in Visual Studio Code.

Open:

```text
news_application/settings.py
```

Check the `DATABASES` section.

Make sure the database settings match the MariaDB installation on your computer.

For example, the database name should match the database created in the previous step.

You may need to change the database username and password to match your own MariaDB installation.

Do not upload passwords or other private credentials to GitHub.

## Step 7: Apply the Database Migrations

The project already contains its migration files, so a new user installing the project does not normally need to create new migrations.

Run:

```powershell
python manage.py migrate
```

This creates the required database tables.

## Step 8: Create an Administrator Account

Create a Django superuser:

```powershell
python manage.py createsuperuser
```

Follow the instructions in PowerShell.

You will be asked for:

- Username
- Email address
- Password

The password will not be displayed while you type it.

## Step 9: Run the Development Server

Start the Django development server:

```powershell
python manage.py runserver
```

Django should display a message similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

Open the address in a web browser:

```text
http://127.0.0.1:8000/
```

The Woodland Chronicle website should now be displayed.

## Step 10: Access the Django Admin

The Django administration area is available at:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser account created earlier.

The admin area can be used to manage users and other administrator-controlled data.

## Step 11: Register a Normal User

Open the website and use the registration page to create a normal account.

The application supports different user roles.

Depending on the role assigned to the account, different features will be available.

## Step 12: Test the Reader Features

A reader can:

- Log in.
- View published articles.
- Subscribe to journalists.
- Subscribe to publishers.
- View articles from subscribed journalists and publishers.
- Read individual articles.

## Step 13: Test the Journalist Features

A journalist can:

- Log in.
- Create an article.
- Edit their articles.
- Delete their articles.
- Submit articles for editor approval.

Articles submitted by journalists will require approval before they are published.

## Step 14: Test the Editor Features

An editor can:

- Log in.
- View pending articles.
- Approve articles.
- Create publishers.
- Edit publishers.
- Delete publishers.
- Manage articles and users.

Once an article is approved, it can become available to readers.

The approval process uses the REST API endpoint:

```text
POST /api/approved/
```

## Step 15: Run the Automated Tests

The project includes automated tests for the application's functionality.

Make sure the virtual environment is active and run:

```powershell
python manage.py test
```

The tests should complete successfully.

## Code Quality

The project uses Flake8 to check Python code style.

Run:

```powershell
flake8 .
```

The project contains a `.flake8` configuration file which sets the maximum line length and excludes the virtual environment and migration files from the checks.

The project also uses `flake8-docstrings` to check Python documentation strings.

## Stopping the Development Server

To stop the Django development server, return to the PowerShell window where it is running and press:

```text
Ctrl + C
```

## REST API Authentication

Protected API endpoints use token authentication.

First obtain a token by sending a POST request to:

```text
/api/token/
```

The request should include the user's username and password.

The returned token can then be included in the request header:

```text
Authorization: Token YOUR_TOKEN_HERE
```

The approval endpoint is:

```text
/api/approved/
```

It requires an authenticated editor.

Example request body:

```json
{
    "article_id": 1
}
```

## Development Notes

This project is intended for educational purposes as part of a Software Engineering course.

The application uses Django's built-in authentication system together with custom user roles for readers, journalists, and editors.

MariaDB is used as the project's database rather than SQLite.

The project also includes a REST API using Django REST Framework.

## Repository

The source code for this project is available on GitHub:

https://github.com/richieboy1995-prog/news-application.git