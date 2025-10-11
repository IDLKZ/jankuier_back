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
3. **ВАЖНО**: Review and edit migration file, especially Foreign Key constraints
4. Apply migration: `alembic upgrade head`
5. **ОБЯЗАТЕЛЬНО**: Verify foreign keys: `python check_foreign_keys.py`

### Foreign Key CASCADE Constraints

**КРИТИЧЕСКАЯ ПРОБЛЕМА**: Alembic может создавать `SET NULL` вместо `CASCADE` даже если в модели указан `ondelete="CASCADE"`.

#### Быстрая справка по CASCADE типам

| Тип | Когда использовать | Пример |
|-----|-------------------|--------|
| **CASCADE** | Зависимые данные без смысла без родителя | `gallery_id`, `item_id`, `material_id` |
| **SET NULL** | Nullable опциональные ссылки | `image_id`, `city_id`, `created_by` |
| **RESTRICT** | Критичные справочники | `status_id`, `role_id` |

#### Правила выбора

```python
# ❌ НЕПРАВИЛЬНО - nullable=False с SET NULL вызовет NotNullViolationError
user_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="SET NULL")]

# ✅ ПРАВИЛЬНО - CASCADE для зависимых данных
gallery_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="CASCADE")]

# ✅ ПРАВИЛЬНО - SET NULL только для nullable полей
image_id: Mapped[DbColumnConstants.ForeignKeyNullableInteger(..., ondelete="SET NULL")]

# ✅ ПРАВИЛЬНО - RESTRICT для справочников
status_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="RESTRICT")]
```

#### Workflow создания FK

1. **В Entity** - выбрать правильный `ForeignKeyInteger` / `ForeignKeyNullableInteger` и `ondelete`
2. **Создать миграцию** - `alembic revision --autogenerate`
3. **⚠️ ПРОВЕРИТЬ миграцию** - убедиться что `sa.ForeignKeyConstraint` содержит `onupdate='CASCADE', ondelete='...'`
4. **Применить** - `alembic upgrade head`
5. **Проверить** - `python check_foreign_keys.py`

#### ORM Cascade Requirements

**КРИТИЧНО**: `ondelete` в Entity **НЕ ДОСТАТОЧНО**! SQLAlchemy требует `cascade` в relationship:

```python
# ❌ НЕПРАВИЛЬНО - вызовет NotNullViolationError
class UserEntity:
    # Entity FK правильный:
    user_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="CASCADE")]

# Parent relationship БЕЗ cascade:
user_code_verifications: Mapped[...] = (
    DbRelationshipConstants.one_to_many(
        target="UserCodeVerificationEntity",
        back_populates="user",
        # ❌ НЕТ cascade! SQLAlchemy попытается установить user_id=NULL
    )
)

# ✅ ПРАВИЛЬНО - оба уровня настроены
class UserEntity:
    # Database CASCADE:
    user_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="CASCADE")]

# ORM CASCADE:
user_code_verifications: Mapped[...] = (
    DbRelationshipConstants.one_to_many(
        target="UserCodeVerificationEntity",
        back_populates="user",
        cascade="all, delete-orphan"  # ✅ Обязательно для зависимых данных!
    )
)
```

**Правило**: Для зависимых данных (carts, verifications, notifications) всегда добавляйте:
1. `ondelete="CASCADE"` в ForeignKey
2. `cascade="all, delete-orphan"` в relationship

**Исключение**: Audit поля (created_by, checked_by) - НЕ добавляйте cascade в relationship

**Подробная документация**: См. `docs/foreign_key_cascade_guide.md` и `README_CASCADE_FIX_COMPLETE.md`

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
- **Validation**: Throws `AppExceptionResponse.bad_request()` if not found

#### 4. By Value - `get_{entity}_by_value_case.py`
- **Purpose**: Retrieve single record by unique value field
- **Parameters**: `value: str`
- **Returns**: `EntityRDTO`
- **Pattern**: Uses `repository.get_first_with_filters()` with `func.lower()` comparison
- **Note**: Only implement if entity has a `value` field with unique constraint
- **Validation**: Throws `AppExceptionResponse.bad_request()` if not found

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

#### Folder Naming Conventions
All entities that support file uploads should follow standardized folder naming patterns:

**Folder Name Constants:**
- `UserFolderName = "users"` - для файлов пользователей
- `FieldFolderName = "fields"` - для файлов полей
- Добавляйте аналогичные константы для новых entities: `{Entity}FolderName = "entity_name"`

**Directory Helper Functions:**
- `user_profile_photo_directory(username)` - Returns `"users/photos/{username}"`
- `field_image_directory(field_value)` - Returns `"fields/images/{field_value}"`
- `application_document_directory(id, department)` - Returns `"applications/documents/{id}/{department}"`

**Pattern for New Entities:**
При создании use case для новых entities с файловой поддержкой:
1. Добавьте `{Entity}FolderName = "entity_name"` в `AppFileExtensionConstants`
2. Создайте helper функцию `{entity}_directory()` следуя паттерну
3. Используйте helper функцию в use cases вместо хардкода путей

```python
# Правильно - используйте helper функции
self.upload_folder = AppFileExtensionConstants.field_image_directory(dto.value)

# Неправильно - хардкод путей
self.upload_folder = f"fields/{dto.value}"
```

## API Architecture and Patterns

### API Structure and Use Cases

The project's API layer (`app/adapters/api/`) follows a consistent pattern where APIs are built on top of Use Cases, providing clean separation between HTTP handling and business logic:

#### Core API Patterns

1. **API Class Structure**: Each API is implemented as a class with `__init__()` and `_add_routes()` methods
2. **Use Case Integration**: APIs directly instantiate and execute Use Cases for all business operations
3. **Route Path Constants**: All paths are defined in `RoutePathConstants` for consistency
4. **Error Handling**: Standardized exception handling with `AppExceptionResponse`

#### Standard CRUD API Routes

All CRUD APIs should implement these standard routes:

- **`GET /`** - Paginated listing (index route)
- **`GET /all`** - Full listing without pagination  
- **`POST /create`** - Create new entity
- **`PUT /update/{id}`** - Update entity by ID
- **`GET /get/{id}`** - Get entity by ID
- **`GET /get-by-value/{value}`** - Get entity by unique value (if applicable)
- **`DELETE /delete/{id}`** - Delete entity by ID

#### Route Path Constants Usage

```python
# Use RoutePathConstants for all route definitions
self.router.get(
    RoutePathConstants.IndexPathName,        # "/"
    RoutePathConstants.AllPathName,          # "/all" 
    RoutePathConstants.CreatePathName,       # "/create"
    RoutePathConstants.UpdatePathName,       # "/update/{id}"
    RoutePathConstants.GetByIdPathName,      # "/get/{id}"
    RoutePathConstants.GetByValuePathName,   # "/get-by-value/{value}"
    RoutePathConstants.DeleteByIdPathName,   # "/delete/{id}"
)

# Path parameters
id: RoutePathConstants.IDPath              # Annotated[int, Path(gt=0, description="Уникальный идентификатор")]
value: RoutePathConstants.ValuePath        # Annotated[str, Path(max_length=255, description="Уникальное значение")]
```

#### Force Delete Query Parameter

For `get`, `get_by_value`, and `delete` endpoints, include the `force_delete` parameter:

```python
async def delete(
    self,
    id: RoutePathConstants.IDPath,
    force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
    db: AsyncSession = Depends(get_db),
) -> bool:
    return await DeleteEntityCase(db).execute(id=id, force_delete=force_delete)
```

#### File Upload Handling

When entities support file uploads, use the FormParserHelper pattern:

```python
async def create(
    self,
    dto: EntityCDTO = Depends(FormParserHelper.parse_entity_dto_from_form),
    file: UploadFile | None = File(default=None),
    db: AsyncSession = Depends(get_db),
) -> EntityWithRelationsRDTO:
    return await CreateEntityCase(db).execute(dto=dto, file=file)
```

#### API Method Pattern

Each API method follows this consistent pattern:

```python
async def method_name(
    self,
    # Parameters (id, dto, filters, etc.)
    db: AsyncSession = Depends(get_db),
) -> ResponseDTO:
    try:
        return await UseCaseClass(db).execute(param1=value1, param2=value2)
    except HTTPException:
        raise
    except Exception as exc:
        raise AppExceptionResponse.internal_error(
            message=i18n.gettext("internal_server_error"),
            extra={"details": str(exc)},
            is_custom=True,
        ) from exc
```

#### Response Models

- **Paginated endpoints**: Use `Pagination{Entity}WithRelationsRDTO`
- **List endpoints**: Use `list[{Entity}WithRelationsRDTO]`
- **Single item endpoints**: Use `{Entity}WithRelationsRDTO` or `{Entity}RDTO`
- **Create/Update endpoints**: Use `{Entity}WithRelationsRDTO` to show relationships
- **Delete endpoints**: Return `bool`

#### Filter Dependencies

- **Pagination filters**: `{Entity}PaginationFilter = Depends()`
- **Basic filters**: `{Entity}Filter = Depends()`
- These are automatically parsed from query parameters

#### Error Handling Standards

All API methods must:
1. Re-raise `HTTPException` without modification
2. Wrap other exceptions in `AppExceptionResponse.internal_error()`
3. Use localized error messages via `i18n.gettext()`
4. Include exception details in `extra` field for debugging

#### FormParserHelper Usage

For entities with file uploads, extend `FormParserHelper` with entity-specific parsing methods:

```python
@staticmethod  
def parse_entity_dto_from_form(
    field1: str = Form(..., description="Field 1"),
    field2: Optional[int] = Form(None, description="Field 2"),
    # ... other fields
) -> EntityCDTO:
    return EntityCDTO(
        field1=field1,
        field2=field2,
        # ... other fields
    )
```

This architecture ensures consistency across all APIs while maintaining clean separation between HTTP concerns and business logic through the Use Case pattern.

## Route Management and Role-Based Access Control

### Route Registration Architecture

The project uses a sophisticated dual-layer route registration system that separates route inclusion from role assignment:

#### Layer 1: Main Route Registration (`app/main.py`)
Main application routes are registered directly in `main.py`:

```python
# Standard entity routes (registered in main.py)
app.include_router(
    AcademyApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/academy",
    tags=["Академии"],
)
```

#### Layer 2: Special Routes System (`app/routes/`)
Critical system routes (user, role, permission) use a separate registration system:

**File Structure:**
- **`app/routes/registry_route.py`** - Main coordinator
- **`app/routes/include_routes.py`** - Route registration for special entities
- **`app/routes/assign_roles.py`** - Role assignment coordinator
- **`app/routes/base_route.py`** - Base role assignment functionality
- **`app/routes/{entity}/{entity}_route.py`** - Entity-specific role assignments

#### Route Constants (`app/shared/route_constants.py`)

**Standard Route Paths:**
```python
class RoutePathConstants:
    # Base paths
    BasePathName = "/api"
    
    # Special entity paths
    RolePathName = "/role"
    PermissionPathName = "/permission" 
    UserPathName = "/user"
    
    # Standard CRUD paths
    IndexPathName = "/"                    # GET /
    AllPathName = "/all"                   # GET /all
    CreatePathName = "/create"             # POST /create
    UpdatePathName = "/update/{id}"        # PUT /update/{id}
    GetByIdPathName = "/get/{id}"         # GET /get/{id}
    DeleteByIdPathName = "/delete/{id}"   # DELETE /delete/{id}
    GetByValuePathName = "/get-by-value/{value}"  # GET /get-by-value/{value}
    
    # Path parameters
    IDPath = Annotated[int, Path(gt=0, description="Уникальный идентификатор")]
    ValuePath = Annotated[str, Path(max_length=255, description="Уникальное значение")]
```

#### Role-Based Access Control

**Role Constants (`app/shared/role_route_constants.py`):**
```python
class RoleRouteConstant:
    AdministratorTagName = "administrator"  # Admin access
    ClientTagName = "client"               # User access  
    CommonTagName = "common"               # Public access
```

**Role Assignment Pattern:**
```python
def assign_entity_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}{RoutePathConstants.EntityPathName}"
    
    # Admin-only endpoints
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.CreatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName]
    )
    
    # Public endpoints  
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
        roles=[RoleRouteConstant.CommonTagName]
    )
```

### Route Registration Workflow

#### For Special Entities (User/Role/Permission):
1. **Route Registration**: `include_routes.py` registers the API routes
2. **Role Assignment**: `assign_roles.py` assigns roles to each endpoint  
3. **Coordination**: `registry_route.py` orchestrates the process
4. **Activation**: `enable_routes(app)` called from middleware or main setup

#### For Standard Entities:
1. **Direct Registration**: Routes registered directly in `main.py`
2. **Manual Role Assignment**: Roles assigned through middleware or decorators if needed

### Best Practices for New API Controllers

#### Standard Entity APIs:
```python
# Register in main.py
app.include_router(
    EntityApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/entity",
    tags=["Entity Name"],
)
```

#### Special System APIs (if needed):
1. Add route registration to `app/routes/include_routes.py`
2. Create `app/routes/entity/entity_route.py` for role assignments
3. Update `app/routes/assign_roles.py` to include the new entity
4. Use `RoutePathConstants` for consistent path naming

#### Consistent Path Naming:
- Always use `RoutePathConstants` for path definitions
- Follow the established CRUD pattern
- Use descriptive prefixes that match entity names
- Include proper tags for API documentation grouping

### Route Security and Authorization

The route management system provides:
- **Centralized role assignment** for critical system endpoints
- **Flexible role-based access control** with multiple role types
- **Consistent path structure** across all APIs
- **Proper separation** between public and administrative functionality
- **Extensible architecture** for adding new entities and roles

This dual-layer approach ensures that critical system routes (user management, roles, permissions) have proper role-based access control while allowing standard business entity routes to be registered simply and efficiently.

## Data Seeding System

### Overview
The project includes a comprehensive seeding system (`app/seeders/`) for populating the database with initial and test data. The system supports both development and production environments with different datasets.

### Core Architecture

#### Seeding Entry Point
- **`app/seeders/runner.py`** - Main entry point that executes all registered seeders
- **Command**: `python -c "import asyncio; from app.seeders.runner import run_seeders; asyncio.run(run_seeders())"`
- **Execution**: Runs all seeders sequentially using async database sessions

#### Base Seeder Pattern
**`app/seeders/base_seeder.py`** provides the abstract foundation:

```python
class BaseSeeder(ABC):
    @abstractmethod
    async def seed(session: AsyncSession) -> None
    @abstractmethod 
    def get_dev_data() -> list
    @abstractmethod
    def get_prod_data() -> list
    @abstractmethod
    def get_dev_updated_data() -> list
    @abstractmethod
    def get_prod_updated_data() -> list
```

#### Environment-Aware Data Loading
- **`get_data()`** - Automatically selects dev/prod data based on `app_config.app_status`
- **`get_updated_data()`** - Environment-specific update data for existing records
- **Environment Detection**: Uses `app_config.app_status` (`"production"` vs development)

#### Core Seeding Methods

**Primary Seeding (`load_seeders`)**:
- Checks if table already contains data (prevents duplicate seeding)
- Inserts data only if table is empty
- Supports PostgreSQL sequence reset after bulk insert
- Logs seeding status and record counts

**Update Seeding (`update_seeders`)**:
- Updates existing records by identification field (usually `id` or `value`)
- Supports adding new records if `add_if_not_exists=True`
- Only updates changed fields (differential updates)
- Handles both entity objects and dictionaries

#### Database Support
- **PostgreSQL**: Full support including sequence reset via `setval()`
- **MySQL**: Basic support (sequence reset not implemented)
- **Transaction Safety**: All operations use database transactions

### Registered Seeders

#### Seeder Registry (`app/seeders/registry.py`)
Execution order ensures proper foreign key dependencies:

1. **`RoleSeeder`** - System roles (Administrator, Client)
2. **`UserSeeder`** - Default admin and client users  
3. **`CountrySeeder`** - Countries from SOTA API service
4. **`SportSeeder`** - Sport types from SOTA API service
5. **`CitySeeder`** - Cities from Ticketon API service (Kazakhstan only)

### Individual Seeder Implementations

#### RoleSeeder (`app/seeders/role/role_seeder.py`)
- **System Roles**: Administrator (admin access) and Client (user access)
- **Data Source**: Hardcoded system roles with multilingual titles
- **Features**: Uses `DbValueConstants` for consistent role IDs and values
- **Properties**: Includes `can_register`, `is_system`, `is_administrative` flags

#### UserSeeder (`app/seeders/user/user_seeder.py`)  
- **Default Users**: Admin user (`admin/admin123`) and client user (`client/client123`)
- **Security**: Uses `get_password_hash()` for secure password storage
- **Data**: Includes sample personal information (names, emails, phones, IIN)
- **Relationships**: Links to appropriate role IDs from `DbValueConstants`

#### External API Seeders
**CountrySeeder** (`app/seeders/country/country_seeder.py`):
- **Data Source**: SOTA API service (`SotaService.get_countries_all_languages()`)
- **Content**: Multi-language country names, SOTA codes, flag images
- **Filtering**: Only includes countries with non-empty Russian names

**SportSeeder** (`app/seeders/sport/sport_seeder.py`):
- **Data Source**: SOTA API service (`SotaService.get_sport_types()`)
- **Content**: Multi-language sport type names
- **Processing**: Uses `slugify()` to generate URL-friendly values

**CitySeeder** (`app/seeders/city/city_seeder.py`):
- **Data Source**: Ticketon API service (`TicketonServiceAPI.get_ticketon_cities()`)
- **Scope**: Kazakhstan cities only (filters by `sota_code = "KZ"`)
- **Dependencies**: Requires CountrySeeder to run first
- **Content**: Multi-language city names, Ticketon IDs and tags

### Seeding Patterns and Best Practices

#### Seeder Implementation Pattern
```python
class EntitySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        # For external API data, check if already populated
        if self.needs_external_data():
            data = await self.fetch_external_data()
            entities = self.get_dev_data() 
        else:
            entities = []
        await self.load_seeders(EntityModel, session, AppTableNames.EntityTableName, entities)

    def get_dev_data(self) -> list[EntityModel]:
        # Transform external data to entity objects
        return [EntityModel(**item_data) for item_data in self.external_data]

    def get_prod_data(self) -> list[EntityModel]:
        return self.get_dev_data()  # Usually same data for both environments
```

#### External API Integration
- **Check Before Fetch**: Verify table is empty before making API calls
- **Error Handling**: Handle API failures gracefully 
- **Data Transformation**: Convert external API formats to entity models
- **Caching**: Store fetched data in instance variables for reuse

#### Multi-language Support
- All seeders include Russian (`title_ru`), Kazakh (`title_kk`), and English (`title_en`) content
- External APIs provide localized data where available
- Fallback strategies for missing translations

### Integration with Application

#### Automatic Sequence Management
- PostgreSQL sequences automatically reset after bulk inserts
- Ensures proper ID generation for subsequent records
- Uses `pg_get_serial_sequence()` for dynamic sequence detection

#### Table Name Constants
- All seeders use `AppTableNames` constants for consistency
- Enables easy table name changes without affecting seeders
- Supports logging and error reporting with correct table names

#### Development Workflow
1. **Initial Setup**: Run seeders after database migration (`alembic upgrade head`)
2. **Development**: Seeders create admin/client users for immediate testing
3. **Production**: Same seeders provide initial system data
4. **Updates**: Use `update_seeders()` for incremental data changes

#### Error Handling and Logging
- Comprehensive logging of seeding operations
- Graceful handling of duplicate data scenarios
- Transaction rollback on failures
- Clear error messages for troubleshooting

This seeding system provides a robust foundation for database initialization, supporting both development convenience and production deployment requirements while maintaining data consistency across environments.

## Development Notes

- The project uses async/await patterns throughout
- Environment variables are managed through `app_config.py`
- Database timezone is configurable (default: Asia/Almaty for PostgreSQL)
- File uploads go to configurable static/upload directories
- All entities support soft deletes via `deleted_at` timestamp
- Use the base repository for consistent CRUD operations
- Follow the use case pattern for business logic
- Critical system routes use the special route management system in `app/routes/`
- Standard business entity routes are registered directly in `main.py`