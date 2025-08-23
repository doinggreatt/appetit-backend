# 🍽️ Appetit - Food Menu Management API

> **Codemasters 3.0 Hackathon Appetit Backend** 🚀

A modern, scalable backend API for food menu management with user authentication and authorization. Built with FastAPI, PostgreSQL, and Docker for the ultimate developer experience.

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based authentication with Argon2 password hashing
- 👥 **User Management** - Complete user CRUD operations with role-based access control
- 🍕 **Food Menu System** - Comprehensive menu management with categories, modifiers, and pricing
- 🐳 **Docker Ready** - Containerized development and production environments
- 📊 **Database Migrations** - Alembic-powered schema management
- 🔄 **Async Operations** - High-performance async database operations
- 📚 **Auto-generated API Docs** - Interactive OpenAPI documentation
- 🛡️ **CORS Enabled** - Cross-origin resource sharing support

## 🏗️ Architecture

```
appetit/
├── src/
│   ├── apps/
│   │   ├── food_menu/     # Menu management system
│   │   └── users/         # User authentication & management
│   ├── config/            # Application configuration
│   └── alembic/           # Database migrations
├── compose/               # Docker configuration
└── docker-compose.*.yml   # Environment-specific setups
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd appetit
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker (Recommended)**
   ```bash
   docker-compose -f docker-compose.local.yml up --build
   ```

4. **Or run locally**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   alembic upgrade head
   
   # Start the server
   uvicorn src.config.app:app --reload --host 0.0.0.0 --port 8080
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8080/api/v1`
   - Interactive Docs: `http://localhost:8080/api/docs`
   - OpenAPI Schema: `http://localhost:8080/api/openapi.json`

## 📖 API Documentation

    - Use swagger 

## 🗄️ Database Schema

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.116+
- **Database**: PostgreSQL with async support
- **ORM**: SQLAlchemy 2.0 with async operations
- **Authentication**: AuthX with JWT tokens
- **Password Hashing**: Argon2-CFFI
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **Python Version**: 3.12+

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/appetit

# JWT Settings
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=true
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose -f docker-compose.local.yml up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📝 Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=src
```

## 📊 API Examples

### Create a User
```bash
curl -X POST "http://localhost:8080/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Authenticate User
```bash
curl -X POST "http://localhost:8080/api/v1/users/authorize" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```


## 📄 License

This project is created for the **Codemasters 3.0 Hackathon**. 

## 👥 Team

Built with ❤️ by the WW team during the hackathon.

---

