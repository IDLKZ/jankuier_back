# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based backend application for a sports licensing service ("Сервис лицензирования ФКК"). The project uses:
- **FastAPI** for the web framework
- **SQLAlchemy** with async support for ORM
- **Alembic** for database migrations
- **Pydantic** for data validation
- **PostgreSQL/MySQL** database support (configurable)

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn (development)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "migration message"

# Run seeders
python -c "import asyncio; from app.seeders.runner import run_seeders; asyncio.run(run_seeders())"
```

### Code Quality
```bash
# Format code
black .
isort .

# Lint code
ruff check .
ruff check . --fix

# Type checking (if mypy is added)
mypy app/
```

## Architecture

### Clean Architecture Pattern
The project follows a clean architecture approach with clear separation of concerns:

- **`app/entities/`** - SQLAlchemy database models/entities
- **`app/adapters/`** - External interface adapters (API, repositories, DTOs)
- **`app/use_case/`** - Business logic use cases
- **`app/core/`** - Core application logic and utilities
- **`app/infrastructure/`** - Infrastructure concerns (database, config)

### Key Components

#### Configuration
- **`app/infrastructure/app_config.py`** - Centralized configuration using Pydantic settings
- Supports both PostgreSQL and MySQL databases
- Environment-based configuration via `.env` file

#### Database Layer
- **`app/infrastructure/db.py`** - Database connection and session management
- **`app/adapters/repository/base_repository.py`** - Generic repository pattern with CRUD operations
- Supports soft deletes, pagination, and filtering

#### Use Cases
- **`app/use_case/base_case.py`** - Abstract base class for all use cases
- All use cases must implement: `execute()`, `validate()`, and optionally `transform()`

#### Entities
- Rich domain models with relationships
- Uses typed SQLAlchemy mappings with custom column constants
- Soft delete support via `deleted_at` field

#### Middleware & CORS
- **`app/middleware/registry_middleware.py`** - Middleware registration
- **`app/core/app_cors.py`** - CORS configuration
- **`app/core/role_docs.py`** - Role-based API documentation

### Features
- **Multi-language support** (i18n) with English, Kazakh, and Russian
- **Role-based access control** with separate API documentation per role
- **File upload handling** with configurable limits
- **Authentication** support (local and Keycloak)
- **Pagination** with generic typing support
- **Soft delete** functionality across entities

## Database

### Supported Databases
- PostgreSQL (default, using asyncpg)
- MySQL (using aiomysql)

### Migration Workflow
1. Make entity changes
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review and edit migration file if needed
4. Apply migration: `alembic upgrade head`

## Development Notes

- The project uses async/await patterns throughout
- Environment variables are managed through `app_config.py`
- Database timezone is configurable (default: Asia/Almaty for PostgreSQL)
- File uploads go to configurable static/upload directories
- All entities support soft deletes via `deleted_at` timestamp
- Use the base repository for consistent CRUD operations
- Follow the use case pattern for business logic