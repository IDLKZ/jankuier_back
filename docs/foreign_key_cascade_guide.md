# Руководство по Foreign Key Cascade Constraints

## Проблема

В проекте возникали ошибки при удалении записей:
```
sqlalchemy.dialects.postgresql.asyncpg.IntegrityError
<class 'asyncpg.exceptions.NotNullViolationError'>: null value in column
```

### Корневая причина

SQLAlchemy и Alembic имеют разные уровни работы с Foreign Keys:

1. **Уровень модели (SQLAlchemy)**: `ondelete="CASCADE"` в `ForeignKey()` - это только **метаданные** для ORM
2. **Уровень базы данных**: Реальные constraints создаются **только через миграции Alembic**
3. **Несоответствие**: Alembic может игнорировать `ondelete` из модели и создавать `SET NULL` по умолчанию

**Результат**:
- В модели указан `ondelete="CASCADE"`
- В БД создан `ON DELETE SET NULL`
- При удалении родительской записи БД пытается установить NULL
- Поле имеет `nullable=False`
- Ошибка: `NotNullViolationError`

## Статистика проблемы

Из 108 foreign keys в проекте:
- ✅ **51 FK** - имеют правильный CASCADE
- ❌ **57 FK** - имеют неправильный SET NULL

## Решение

### 1. Применить миграцию исправления

```bash
# Применить миграцию исправления всех FK
alembic upgrade head

# Проверить результат
python check_foreign_keys.py
```

### 2. Понимать типы CASCADE constraints

#### CASCADE - Каскадное удаление
**Используется для**: Зависимых данных, которые не имеют смысла без родительской записи

```python
# Примеры: galleries, materials, items
gallery_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(
        AppTableNames.GroupTableName,
        onupdate="CASCADE",
        ondelete="CASCADE"  # ✅ Удаляются вместе с группой
    )
]
```

**Миграция**:
```python
op.create_foreign_key(
    'academy_galleries_group_id_fkey',
    'academy_galleries', 'academy_groups',
    ['group_id'], ['id'],
    onupdate='CASCADE', ondelete='CASCADE'
)
```

#### SET NULL - Установка NULL
**Используется для**: Nullable опциональных ссылок

```python
# Примеры: image_id, optional references
image_id: Mapped[
    DbColumnConstants.ForeignKeyNullableInteger(  # ✅ nullable=True
        AppTableNames.FileTableName,
        onupdate="CASCADE",
        ondelete="SET NULL"  # ✅ Устанавливает NULL при удалении файла
    )
]
```

**Миграция**:
```python
op.create_foreign_key(
    'users_image_id_fkey',
    'users', 'files',
    ['image_id'], ['id'],
    onupdate='CASCADE', ondelete='SET NULL'
)
```

#### RESTRICT - Запрет удаления
**Используется для**: Критичных справочников (статусы, роли)

```python
# Примеры: status_id, role_id
status_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(
        AppTableNames.StatusTableName,
        onupdate="CASCADE",
        ondelete="RESTRICT"  # ✅ Запрещает удаление используемого статуса
    )
]
```

**Миграция**:
```python
op.create_foreign_key(
    'payment_transactions_status_id_fkey',
    'payment_transactions', 'payment_transaction_statuses',
    ['status_id'], ['id'],
    onupdate='CASCADE', ondelete='RESTRICT'
)
```

## Правила выбора CASCADE типа

### Матрица принятия решений

| Тип поля | nullable | Смысл без родителя | CASCADE тип | Пример |
|----------|----------|-------------------|-------------|--------|
| Зависимые данные | False | ❌ Нет | **CASCADE** | galleries, items, materials |
| Опциональная ссылка | True | ✅ Да | **SET NULL** | image_id, city_id, created_by |
| Критичный справочник | False | ✅ Да | **RESTRICT** | status_id, role_id |
| Audit/History поля | True | ✅ Да | **SET NULL** | canceled_by, approved_by |

### Примеры из проекта

```python
# ❌ НЕПРАВИЛЬНО - nullable=False с SET NULL
user_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(  # nullable=False
        AppTableNames.UserTableName,
        ondelete="SET NULL"  # ❌ Вызовет NotNullViolationError
    )
]

# ✅ ПРАВИЛЬНО - nullable=False с CASCADE
user_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(  # nullable=False
        AppTableNames.UserTableName,
        ondelete="CASCADE"  # ✅ Запись удалится вместе с user
    )
]

# ✅ ПРАВИЛЬНО - nullable=True с SET NULL
user_id: Mapped[
    DbColumnConstants.ForeignKeyNullableInteger(  # nullable=True
        AppTableNames.UserTableName,
        ondelete="SET NULL"  # ✅ Поле станет NULL
    )
]

# ✅ ПРАВИЛЬНО - nullable=False с RESTRICT
status_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(  # nullable=False
        AppTableNames.StatusTableName,
        ondelete="RESTRICT"  # ✅ Запретит удаление используемого статуса
    )
]
```

## Workflow создания новых FK

### 1. Определение в Entity

```python
# Шаг 1: Определите тип связи
# Зависимые данные - CASCADE
gallery_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(
        AppTableNames.GroupTableName,
        onupdate="CASCADE",
        ondelete="CASCADE"
    )
]

# Опциональная ссылка - SET NULL
image_id: Mapped[
    DbColumnConstants.ForeignKeyNullableInteger(
        AppTableNames.FileTableName,
        onupdate="CASCADE",
        ondelete="SET NULL"
    )
]

# Критичный справочник - RESTRICT
status_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(
        AppTableNames.StatusTableName,
        onupdate="CASCADE",
        ondelete="RESTRICT"
    )
]
```

### 2. Создание миграции

```bash
alembic revision --autogenerate -m "add_entity_table"
```

### 3. ВАЖНО: Проверка миграции

**⚠️ НЕ ДОВЕРЯЙТЕ АВТОГЕНЕРАЦИИ!**

Alembic может создать неправильный constraint:

```python
# ❌ Alembic может сгенерировать:
sa.ForeignKeyConstraint(['user_id'], ['users.id'])  # без ondelete!

# ✅ Исправьте на:
sa.ForeignKeyConstraint(
    ['user_id'], ['users.id'],
    onupdate='CASCADE',
    ondelete='CASCADE'  # или SET NULL / RESTRICT
)
```

### 4. Проверка после миграции

```bash
# Применить миграцию
alembic upgrade head

# Проверить FK в БД
python check_foreign_keys.py
```

## Relationship CASCADE в ORM

**ВАЖНО**: CASCADE в `ForeignKey` (БД) и CASCADE в `relationship` (ORM) - **это разные вещи!**

### Database CASCADE vs ORM CASCADE

```python
# DATABASE CASCADE - работает на уровне БД
user_id: Mapped[
    DbColumnConstants.ForeignKeyInteger(
        AppTableNames.UserTableName,
        ondelete="CASCADE"  # ← Это для БД PostgreSQL/MySQL
    )
]

# ORM CASCADE - работает на уровне SQLAlchemy
user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
    target=AppEntityNames.UserEntityName,
    cascade="all, delete-orphan"  # ← Это для SQLAlchemy ORM
)
```

### Когда использовать ORM CASCADE

```python
# Parent entity
class User:
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # ← ORM удалит posts при session.delete(user)
    )

# Child entity
class Post:
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            "users",
            ondelete="CASCADE"  # ← БД удалит posts при DELETE FROM users
        )
    ]
```

**Рекомендация**: Используйте **оба уровня** для надежности:
- **DB CASCADE**: Защита на уровне БД (работает всегда)
- **ORM CASCADE**: Удобство работы через SQLAlchemy session

## Soft Delete и CASCADE

**ПРОБЛЕМА**: Проект использует Soft Delete через `deleted_at`, что конфликтует с DB CASCADE.

### Решение для Soft Delete

```python
# В BaseRepository.delete()
async def delete(self, id: int, force_delete: bool = False) -> bool:
    obj = await self.get(id, include_deleted_filter=True)
    if not obj:
        raise AppExceptionResponse.bad_request(message="Не найдено")

    if hasattr(obj, "deleted_at") and not force_delete:
        # Soft delete - вручную обработать зависимости
        await self._soft_delete_dependencies(obj)
        setattr(obj, "deleted_at", datetime.utcnow())
    else:
        # Hard delete - DB CASCADE сработает автоматически
        await self.db.delete(obj)

    await self.db.commit()
    return True
```

### Рекомендация: Используйте force_delete для CASCADE

```python
# Use Case удаления с зависимостями
async def execute(self, id: int) -> bool:
    # Для записей с зависимостями используйте force_delete=True
    # Это позволит DB CASCADE удалить все связанные записи
    return await self.repository.delete(id, force_delete=True)
```

## Проверка и мониторинг

### Скрипт проверки FK

```bash
# Проверить все FK в БД
python check_foreign_keys.py
```

Скрипт покажет все FK без CASCADE:
```
[!] product_galleries.file_id -> files.id
   UPDATE: CASCADE, DELETE: SET NULL  # ← Должно быть CASCADE!
```

### SQL запрос для ручной проверки

```sql
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND rc.delete_rule != 'CASCADE'
ORDER BY tc.table_name;
```

## Чек-лист для разработчиков

При создании новой Entity с FK:

- [ ] Определить тип связи (зависимые / опциональные / справочник)
- [ ] Выбрать правильный `ForeignKeyInteger` или `ForeignKeyNullableInteger`
- [ ] Указать правильный `ondelete` (CASCADE / SET NULL / RESTRICT)
- [ ] Создать миграцию через `alembic revision --autogenerate`
- [ ] **ПРОВЕРИТЬ** сгенерированную миграцию на правильность `ondelete`
- [ ] Применить миграцию `alembic upgrade head`
- [ ] Запустить `python check_foreign_keys.py` для проверки
- [ ] Настроить `relationship` cascade если нужно
- [ ] Обработать Soft Delete в Use Case если требуется

## Частые ошибки

### ❌ Ошибка 1: Доверие автогенерации
```python
# Alembic сгенерировал без ondelete
sa.ForeignKeyConstraint(['user_id'], ['users.id'])
```
**Решение**: Всегда явно указывайте `onupdate` и `ondelete`

### ❌ Ошибка 2: SET NULL на NOT NULL поле
```python
# nullable=False
user_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="SET NULL")]
```
**Решение**: Используйте `CASCADE` или `RESTRICT` для NOT NULL

### ❌ Ошибка 3: CASCADE на критичные справочники
```python
# Удаление роли удалит всех пользователей!
role_id: Mapped[DbColumnConstants.ForeignKeyInteger(..., ondelete="CASCADE")]
```
**Решение**: Используйте `RESTRICT` для справочников

### ❌ Ошибка 4: Путаница DB и ORM CASCADE
```python
# Это не влияет на БД!
relationship("User", cascade="all, delete-orphan")
```
**Решение**: Настройте CASCADE на обоих уровнях

## Заключение

**Ключевые принципы**:
1. `ondelete` в модели - это только **метаданные**
2. Реальный constraint создается **только в миграции**
3. **Всегда проверяйте** миграции вручную
4. Используйте `check_foreign_keys.py` после каждой миграции
5. Выбирайте CASCADE тип на основе **бизнес-логики**, а не удобства

**Применение миграции исправления**:
```bash
alembic upgrade head
python check_foreign_keys.py  # Должно показать 0 ошибок
```
