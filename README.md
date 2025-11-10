# Levitica HR Management System

A comprehensive HR Management System built with FastAPI, featuring multi-role authentication and admin management.

## Features

- ✅ **Multi-Role Authentication** (Superadmin, Admin, User)
- ✅ **JWT Token-based Security**
- ✅ **Admin Account Management** (Superadmin only)
- ✅ **Profile Image Upload** (Max 4MB)
- ✅ **RESTful API** with OpenAPI documentation
- ✅ **SQLAlchemy ORM** with support for SQLite/PostgreSQL/MySQL
- ✅ **Clean Architecture** (Repository-Service-Controller pattern)

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd hr-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python scripts/init_db.py
python scripts/setup.py

Running the Application
Bash

uvicorn app.main:app --reload
The API will be available at:

API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Default Superadmin Credentials
text

Email: superadmin@levitica.com
Password: SuperAdmin@123
⚠️ IMPORTANT: Change the default password after first login!

API Endpoints
Authentication
POST /api/v1/auth/login - Login
GET /api/v1/auth/me - Get current user
POST /api/v1/auth/logout - Logout
Superadmin (Requires Superadmin Role)
POST /api/v1/superadmin/admins - Create admin
GET /api/v1/superadmin/admins - List admins
GET /api/v1/superadmin/admins/{id} - Get admin details
PUT /api/v1/superadmin/admins/{id} - Update admin
DELETE /api/v1/superadmin/admins/{id} - Delete admin
File Upload
POST /api/v1/upload/profile-image - Upload profile image
System
GET /api/v1/health - Health check
Project Structure
text

hr-management-system/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── superadmin.py
│   │   │   ├── files.py
│   │   │   └── health.py
│   │   ├── deps.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── base.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── enums.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services/
│   │   ├── admin_service.py
│   │   └── auth_service.py
│   └── main.py
├── scripts/
│   └── init_db.py
├── .env.example
├── requirements.txt
└── README.md
Development
Running Tests
Bash

pytest
Database Migrations
Bash
# run
python scripts/setup.py

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
Security Notes
Change SECRET_KEY in .env
Change default superadmin password
Use environment variables for sensitive data
Enable HTTPS in production
Configure CORS properly for production
Use PostgreSQL/MySQL instead of SQLite for production
