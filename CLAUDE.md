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

## Use Case CRUD Patterns

### Standard Use Case Structure
All use cases must implement the BaseUseCase pattern with three required methods:

1. **`execute(*args, **kwargs) -> T`** - Main entry point and business logic execution
2. **`validate(*args, **kwargs)`** - Input validation and business rule checks
3. **`transform(*args, **kwargs)`** - Optional data transformation (can be empty)

### Read Operations Pattern
For entities with CRUD operations, implement these 4 standard read use cases:

#### 1. All Data - `all_{entity}_case.py`
- **Purpose**: Retrieve all records with filtering and sorting
- **Parameters**: Filter object with search, order_by, order_direction, is_show_deleted
- **Returns**: `list[EntityRDTO]`
- **Pattern**: Uses `repository.get_with_filters()` or `repository.get_all()`

#### 2. Paginated Data - `paginate_{entity}_case.py`
- **Purpose**: Retrieve paginated records
- **Parameters**: PaginationFilter object (extends base filter with page/per_page)
- **Returns**: `Pagination{Entity}RDTO` (specific pagination DTO)
- **Pattern**: Uses `repository.paginate(dto=EntityRDTO, ...)`
- **Required**: Must use PaginationDTO for response

#### 3. By ID - `get_{entity}_by_id_case.py`
- **Purpose**: Retrieve single record by primary key
- **Parameters**: `id: int`
- **Returns**: `EntityRDTO`
- **Pattern**: Uses `repository.get(id, include_deleted_filter=True)`
- **Validation**: Throws `AppExceptionResponse.not_found()` if not found

#### 4. By Value - `get_{entity}_by_value_case.py`
- **Purpose**: Retrieve single record by unique value field
- **Parameters**: `value: str`
- **Returns**: `EntityRDTO`
- **Pattern**: Uses `repository.get_first_with_filters()` with `func.lower()` comparison
- **Note**: Only implement if entity has a `value` field with unique constraint
- **Validation**: Throws `AppExceptionResponse.not_found()` if not found

### CRUD Use Case Conventions

#### Create Use Case
- Validates uniqueness of `value` field if present
- Auto-generates `value` from `title_ru` using `DbValueConstants.get_value()` if not provided
- Uses `repository.create()` and refreshes with relationships

#### Update Use Case
- Validates entity exists and uniqueness constraints
- Excludes current record from uniqueness check using `model.id != id`
- Uses `repository.update(obj, dto)` pattern

#### Delete Use Case
- Supports soft delete (default) and force delete
- Validates entity exists before deletion
- May include business rules (e.g., cannot delete system roles)
- Uses `repository.delete(id, force_delete=False)`

### Filter and DTO Patterns

#### Filters
- **Base Filter**: For `all_` use cases (search, sorting, show_deleted)
- **Pagination Filter**: Extends base filter with page/per_page parameters
- Implements `apply()` method returning list of SQLAlchemy filters
- Search typically covers title fields (title_ru, title_kk, title_en) and value

#### DTOs
- **CDTO**: Create Data Transfer Object for input
- **RDTO**: Read Data Transfer Object for output
- **Pagination{Entity}RDTO**: Specific pagination response with typed items list

### User CRUD Patterns (Extended Example)

#### User Entity Features
- Has multiple unique fields: `username`, `email`, `phone`, `iin`
- Supports file uploads through `image_id` foreign key to FileEntity
- Password hashing during create/update operations
- Complex validation for multiple unique constraints

#### User Read Operations
1. **`all_user_case.py`** - Returns `list[UserWithRelationsRDTO]` with relationships
2. **`paginate_user_case.py`** - Returns `PaginationUserWithRelationsRDTO`
3. **`get_user_by_id_case.py`** - Standard ID lookup
4. **`get_user_by_username_case.py`** - By unique `username` field (not `value`)

#### User CUD Operations with File Handling
- **Create**: Validates uniqueness of username/email/phone/iin, handles optional file upload
- **Update**: Preserves password if not changed, handles file update/replacement
- **Delete**: Soft delete with automatic file cleanup via FileService

## File Service Integration

### FileService Overview
The `FileService` class (`app/infrastructure/service/file_service.py`) provides comprehensive file handling:

#### Core Methods
1. **`save_file(file, uploaded_folder, extensions)`** - Upload new file
2. **`update_file(file_id, new_file, uploaded_folder, extensions)`** - Replace existing file
3. **`delete_file(file_id)`** - Remove file from disk and database
4. **`read_file_base64(file_id)`** - Read file as Base64 string
5. **`save_from_bytes(file_bytes, filename, uploaded_folder)`** - Save from byte data

#### File Validation
- **Extension validation**: Checks against allowed extensions from `AppFileExtensionConstants`
- **Size validation**: Configurable max file size (default from `app_config.app_upload_max_file_size_mb`)
- **Security**: Blocks files with extensions in `not_allowed_extensions`

#### File Storage
- **Path generation**: UUID-based unique filenames to prevent conflicts
- **Directory structure**: Organized by entity type (e.g., `users/photos/{username}`)
- **File metadata**: Stored in `FileEntity` with filename, path, size, content_type

#### Usage in Use Cases
```python
# In __init__
self.file_service = FileService(db)
self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

# In validate() 
if file:
    self.file_service.validate_file(file, self.extensions)

# In transform() - Create
if file:
    file_entity = await self.file_service.save_file(
        file, self.upload_folder, self.extensions
    )
    dto.image_id = file_entity.id

# In transform() - Update  
if file:
    if self.model.image_id:
        # Replace existing file
        file_entity = await self.file_service.update_file(
            file_id=self.model.image_id,
            new_file=file,
            uploaded_folder=self.upload_folder,
            extensions=self.extensions,
        )
    else:
        # Create new file
        file_entity = await self.file_service.save_file(...)
    dto.image_id = file_entity.id

# In delete use case
if self.model.image_id:
    await self.file_service.delete_file(file_id=self.model.image_id)
```

#### File Extension Constants
`AppFileExtensionConstants` provides predefined extension sets:
- `IMAGE_EXTENSIONS` - jpg, png, gif, svg, webp, etc.
- `VIDEO_EXTENSIONS` - mp4, avi, mkv, mov, etc.
- `AUDIO_EXTENSIONS` - mp3, wav, aac, flac, etc.
- `DOCUMENT_EXTENSIONS` - pdf, doc, xls, ppt, txt, etc.
- `ALL_EXTENSIONS` - Combined set of all above

#### Directory Helpers
- `user_profile_photo_directory(username)` - Returns `"users/photos/{username}"`
- `application_document_directory(id, department)` - Returns `"applications/documents/{id}/{department}"`

## Development Notes

- The project uses async/await patterns throughout
- Environment variables are managed through `app_config.py`
- Database timezone is configurable (default: Asia/Almaty for PostgreSQL)
- File uploads go to configurable static/upload directories
- All entities support soft deletes via `deleted_at` timestamp
- Use the base repository for consistent CRUD operations
- Follow the use case pattern for business logic