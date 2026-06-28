# StudySprint Backend — Django REST Framework + JWT + PostgreSQL

Tested end-to-end: register → login → subjects CRUD → tasks CRUD + filters →
complete task → save focus session → dashboard stats → logout. All working.

## Folder Structure

```
studysprint-backend/
├── manage.py
├── requirements.txt
├── .env.example
├── studysprint_backend/      # project settings, urls
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                 # register, login, logout, JWT
├── subjects/                 # Subject CRUD
├── tasks/                    # Task CRUD + filters (subject/priority/status/due_date)
├── focus_sessions/           # Pomodoro session history
└── dashboard/                # overview, daily progress, weekly stats
```

## 1. Install Python & PostgreSQL

- Python 3.10+ installed honi chahiye
- PostgreSQL installed aur running honi chahiye (PgAdmin ya `psql` se bhi check kar sakte ho)

Create the database (psql ya pgAdmin se):
```sql
CREATE DATABASE studysprint_db;
```

## 2. Setup virtual environment

```bash
cd studysprint-backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your real PostgreSQL credentials:

```bash
cp .env.example .env
```

`.env` file:
```
DEBUG=True
SECRET_KEY=django-insecure-change-this-key-in-production
USE_POSTGRES=True
DB_NAME=studysprint_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

> Agar PostgreSQL install karne ka time nahi hai, `USE_POSTGRES=False` set kar do —
> app automatically SQLite use karega, bina kisi code change ke. Submission ke
> baad PostgreSQL pe switch karna ho to sirf `.env` change karna padega.

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create an admin user (optional, for Django admin panel)

```bash
python manage.py createsuperuser
```

## 7. Run the server

```bash
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000/**
Django admin: **http://127.0.0.1:8000/admin/**

## API Endpoints

### Auth (`/api/auth/`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login → returns `{access, refresh}` |
| POST | `/api/auth/login/refresh/` | Refresh access token |
| POST | `/api/auth/logout/` | Logout (blacklists refresh token) |
| GET | `/api/auth/me/` | Current logged-in user profile |

### Subjects (`/api/subjects/`)
| Method | Endpoint |
|---|---|
| GET | `/api/subjects/` |
| POST | `/api/subjects/` |
| GET/PUT/PATCH/DELETE | `/api/subjects/{id}/` |

### Tasks (`/api/tasks/`)
| Method | Endpoint |
|---|---|
| GET | `/api/tasks/` (filters: `?subject=1&priority=high&is_completed=false&due_date=2026-06-30`) |
| POST | `/api/tasks/` |
| GET/PUT/PATCH/DELETE | `/api/tasks/{id}/` |
| POST | `/api/tasks/{id}/complete/` |
| POST | `/api/tasks/{id}/uncomplete/` |

### Focus Sessions (`/api/sessions/`)
| Method | Endpoint |
|---|---|
| GET | `/api/sessions/` |
| POST | `/api/sessions/` — body: `{task, duration_minutes, completed_at}` |

### Dashboard (`/api/dashboard/`)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/overview/` | total focus time, completed tasks, recent sessions |
| GET | `/api/dashboard/daily-progress/?days=7` | per-day focus minutes |
| GET | `/api/dashboard/weekly-stats/` | weekly totals + daily breakdown |

## Authentication header

All protected endpoints need:
```
Authorization: Bearer <access_token>
```

## Notes for the frontend dev

- CORS is already configured for `http://localhost:5173` (Vite) and `http://localhost:3000` (CRA).
- All list endpoints are paginated (DRF `PageNumberPagination`, 20 per page) — response shape is `{count, next, previous, results}`.
- Every user only sees their own subjects/tasks/sessions (filtered server-side by `request.user`).
