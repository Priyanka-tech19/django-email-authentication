# Django Email Authentication System

A Django web application that provides user registration with email verification, login/logout, password reset, and profile management.

## Features

- **User Registration:** Register with a username, email address, and password.
- **Email Verification:** Activate a newly registered account through an email verification link.
- **Authentication:** Login and logout using Django's built-in authentication system.
- **Protected Dashboard:** Restrict dashboard access to authenticated users.
- **Profile Management:** Upload and update a profile picture.
- **Automatic Profile Creation:** Create user profiles using Django signals.
- **Password Reset:** Password recovery using Django's built-in password reset views.
- **Database Integration:** PostgreSQL database support.
- **Environment Configuration:** Manage sensitive settings using environment variables.

## Tech Stack

- Python
- Django
- PostgreSQL
- HTML and CSS
- Pillow
- python-dotenv

## Project Structure

```text id="w4g7ni"
django-email-authentication/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── dashboard.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── password_reset.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── register.html
│   │       ├── update_profile.html
│   │       └── upload_profile_pic.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── tokens.py
│   ├── urls.py
│   └── views.py
├── auth/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .gitignore
```

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash id="7ch8of"
git clone https://github.com/Priyanka-tech19/django-email-authentication.git
cd django-email-authentication
```

### 2. Create and activate a virtual environment

For Windows PowerShell:

```powershell id="zv8v5w"
python -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash id="g5x1g4"
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the same directory as `manage.py`.

Add the following variables and replace the placeholder values with your own configuration:

```env id="m83b8w"
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your_database_name
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_email_app_password
```

**Important:** These are example values. Never commit your actual `.env` file or expose your secret key, database password, or email credentials on GitHub. For Gmail, use an app password if required.

### 5. Set up PostgreSQL

Install PostgreSQL and create a database for the project. Update the database name, username, password, host, and port in your `.env` file.

### 6. Apply database migrations

```bash id="m8d9f1"
python manage.py migrate
```

### 7. Create an administrator account (optional)

```bash id="a5h2cd"
python manage.py createsuperuser
```

### 8. Run the development server

```bash id="g2j7kx"
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

**Note:** The project is configured for local development. Email verification currently uses a localhost activation link, so the link is intended for testing on the same computer.

## Application URLs

| Feature | URL |
|---|---|
| Registration | `/accounts/register/` |
| Login | `/accounts/login/` |
| Logout | `/accounts/logout/` |
| Dashboard | `/accounts/dashboard/` |
| Profile Update | `/accounts/update-profile/` |
| Password Reset | `/accounts/password-reset/` |

## Key Implementation Details

- Used Django's built-in `User` model for authentication.
- Implemented email activation using a UID and token.
- Used a one-to-one relationship between `User` and `Profile`.
- Used Django signals for automatic profile creation.
- Implemented profile picture uploads using Django forms and Pillow.
- Configured PostgreSQL and environment variables for local development.

## Future Improvements

- Add automated tests for registration, activation, login, and profile management.
- Improve email templates and user-facing error messages.
- Configure production-ready settings and deployment.

## Author

**Priyanka**

GitHub: [Priyanka-tech19](https://github.com/Priyanka-tech19)
