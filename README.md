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
2. Copy `.env.example` to `.env` and update PostgreSQL credentials.
3. Activate virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create admin user (optional, default is admin/Admin@12345):

```bash
python manage.py createsuperuser
```

7. Start server:

```bash
python manage.py runserver
```

8. Open in browser:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Login: admin / Admin@12345

## Default Navigation

- Dashboard
- Books
- Add Copy (Librarian+)
- Members
- Issue Book (Assistant+)
- Return Book (Assistant+)
- Loans
- Admin (Staff only)

## Role-Based Access Control (RBAC)

Four user roles with different permissions:

| Role | Dashboard | Books | Add Copy | Members | Issue/Return | Admin |
|------|-----------|-------|---------|---------|--------------|-------|
| **Administrator** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Librarian** | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| **Assistant** | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| **Viewer** | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

Assign roles in Django admin:
1. Go to `/admin/`
2. Navigate to Users
3. Edit a user and set their Staff Profile role
4. Save

## Notes

- If you want SQLite for quick testing, set `DB_ENGINE=sqlite3` in `.env`.
- For production, set `DEBUG=false` and use a strong `SECRET_KEY`.
- Default superuser: admin / Admin@12345 (change this after first login).
