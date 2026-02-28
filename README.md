# NLF Database Application

Professional Database Management System with Vue.js Frontend and FastAPI Backend.

## Features

- ✅ User Authentication with JWT tokens
- ✅ Two-Factor Authentication (OTP)
- ✅ Role-Based Access Control (RBAC)
- ✅ User Registration with Email Verification
- ✅ Password Reset Functionality
- ✅ Email Change with Verification
- ✅ User Profile Management
- ✅ Support Team User Management
- ✅ Multi-language Support (English, German)
- ✅ PostgreSQL Database with SQLAlchemy ORM
- ✅ Alembic migrations support for schema changes
- ✅ RESTful API with FastAPI
- ✅ Vue.js 3 Frontend with Pinia Store
- ✅ Comprehensive Unit Tests

## Requirements

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Visual Studio Code

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt

# Configure .env file (copy from .env.example)
cp .env.example .env

# Initialize database
python scripts/init_db.py

# Start development server
python -m app.main
```

Backend runs at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install

# Configure .env.local file (copy from .env.example)
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

## Documentation

- [Installation & Setup Guide](install.md)
- [API Documentation](http://localhost:8000/docs) (Swagger UI)
- [API ReDoc](http://localhost:8000/redoc)

## Project Structure

```
nlf/db/
├── backend/           # Python FastAPI backend
│   ├── app/          # Main application
│   ├── scripts/      # Database initialization
│   ├── tests/        # Backend unit tests
│   └── config.py     # Configuration
│
├── frontend/         # Vue.js frontend
│   ├── src/         # Source code
│   ├── tests/       # Frontend unit tests
│   └── vite.config.js
│
└── install.md        # Setup guide
```

## Testing

### Backend
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend
```bash
cd frontend
npm run test
```

## Database

### Create Databases
```sql
CREATE USER nlf_user WITH PASSWORD 'nlf_password';
CREATE DATABASE nlf_db OWNER nlf_user;
CREATE DATABASE nlf_db_test OWNER nlf_user;
```

### Models
- **User** - User accounts with authentication
- **Role** - User roles (admin, support, user)
- **Permission** - Granular permissions
- **UserRole** - User-to-role mapping
- **RolePermission** - Role-to-permission mapping

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/password-reset` - Request password reset

### User Profile
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update profile
- `POST /api/v1/users/password-change` - Change password
- `POST /api/v1/users/email-change` - Change email

### User Management (Admin/Support)
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user

## Environment Variables

### Backend (.env)
```env
ENVIRONMENT=development
DB_HOST=localhost
DB_PORT=5432
DB_USER=nlf_user
DB_PASSWORD=nlf_password
DB_NAME=nlf_db
SECRET_KEY=your-secret-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Write/update tests
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request

## Code Quality

- Backend: Python with Black, Flake8, isort
- Frontend: JavaScript/Vue with ESLint

```bash
# Backend
cd backend
black app tests
flake8 app tests

# Frontend
cd frontend
npm run lint
```

## Security

⚠️ **Important Notes:**
- Change SECRET_KEY in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting
- Regular dependency updates

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the [Installation Guide](install.md)
2. Review API Documentation
3. Create a GitHub Issue

## Author

Your Company

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-28
