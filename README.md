# Library Management System (Django + PostgreSQL)

A complete Library Management System built with Django and PostgreSQL-ready configuration.

## Features

- Secure authentication (login/logout)
- Dashboard with KPI cards and recent circulation
- Book catalog management
- Book copy management (accession numbers)
- Member management
- Issue and return workflows
- Automatic overdue fine calculation
- Django admin for full data control
- Professional responsive UI

## Tech Stack

- Django 4.2
- PostgreSQL
- Bootstrap 5 + custom CSS

## Setup

1. Create a PostgreSQL database named `library_db`.
2. Copy `.env.example` to `.env` and update credentials.
3. Install dependencies:

```powershell
C:/Users/PRAVEEN/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt
```

4. Run migrations:

```powershell
C:/Users/PRAVEEN/AppData/Local/Programs/Python/Python311/python.exe manage.py makemigrations
C:/Users/PRAVEEN/AppData/Local/Programs/Python/Python311/python.exe manage.py migrate
```

5. Create admin user:

```powershell
C:/Users/PRAVEEN/AppData/Local/Programs/Python/Python311/python.exe manage.py createsuperuser
```

6. Start server:

```powershell
C:/Users/PRAVEEN/AppData/Local/Programs/Python/Python311/python.exe manage.py runserver
```

7. Open:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Default Navigation

- Dashboard
- Books
- Add Copy
- Members
- Issue Book
- Return Book
- Loans
- Admin

## Notes

- If you want SQLite for quick testing, set `DB_ENGINE=sqlite3` in `.env`.
- For production, set `DEBUG=false` and use a strong `SECRET_KEY`.
