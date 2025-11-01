# Locust Load Testing - Validation Fixes

## Проблема

При запуске Locust тестов авторизация возвращала **HTTP 422 (Validation Error)** из-за несоответствия данных валидационным требованиям проекта.

## Анализ валидационных требований

### 1. Пароли (PASSWORD_REGEX)
```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).{8,}$
```

**Требования:**
- Минимум 8 символов
- Хотя бы одна строчная буква (a-z)
- Хотя бы одна заглавная буква (A-Z)
- Хотя бы одна цифра (0-9)
- Хотя бы один спецсимвол из списка: `!@#$%^&*()_-+=`

### 2. Номер телефона (KZ_MOBILE_REGEX)
```regex
^77\d{9}$
```

**Требования:**
- Формат: `77XXXXXXXXX` (11 цифр, начинается с 77)
- БЕЗ знака "+" в начале

### 3. Логин (LOGIN_REGEX)
```regex
^[a-zA-Z0-9._@-]{3,255}$
```

**Требования:**
- От 3 до 255 символов
- Только буквы, цифры и символы: `._@-`

## Найденные проблемы

### Проблема 1: Пароли в seeder
**Файл:** `app/seeders/user/user_seeder.py`

**Было:**
```python
password_hash=get_password_hash("admin123")   # admin
password_hash=get_password_hash("admin123")   # client
```

**Проблемы:**
- Нет заглавной буквы
- Нет спецсимвола

**Стало:**
```python
password_hash=get_password_hash("Admin123!")  # admin
password_hash=get_password_hash("Client123!") # client
```

### Проблема 2: Отсутствие поля IIN
**Файл:** `locustfile.py` (строка 89)

**Проблема:** Поле `iin` обязательное в RegisterDTO, но не было включено в payload

**Стало:**
```python
"iin": f"{random.randint(100000000000, 999999999999)}",  # 12-digit IIN
"patronomic": None,  # Опциональное отчество
```

### Проблема 3: Телефон в регистрации
**Файл:** `locustfile.py` (строка 93)

**Было:**
```python
"phone": f"+7{random.randint(7000000000, 7999999999)}"  # +77XXXXXXXXX
```

**Проблема:** Знак "+" не допускается регулярным выражением

**Стало:**
```python
"phone": f"77{random.randint(700000000, 799999999)}"    # 77XXXXXXXXX
```

### Проблема 4: Пароли в тестах логина
**Файл:** `locustfile.py`

**Было:**
```python
# ProductBrowserUser (строка 182)
"password": "client123"

# AdminOperationsUser (строка 344)
"password": "admin123"

# MixedOperationsUser (строка 435)
"password": "client123"
```

**Стало:**
```python
# ProductBrowserUser
"password": "Client123!"

# AdminOperationsUser
"password": "Admin123!"

# MixedOperationsUser
"password": "Client123!"
```

## Результаты тестирования

### Успешный тест регистрации
```bash
$ curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d @test_register.json

# Результат: HTTP 200 OK
# Пользователь успешно создан с id=4
```

### Успешный тест авторизации
```bash
$ curl -X POST "http://127.0.0.1:8000/api/auth/login-client" \
  -H "Content-Type: application/json" \
  -d '{"username":"client","password":"Client123!"}'

# Результат: HTTP 200 OK
# Получены access_token и refresh_token
```

### Результаты Locust нагрузочного тестирования
```
# Команда: locust --host=http://127.0.0.1:8000 AuthUser --users 3 --spawn-rate 1 --run-time 15s --headless

POST /api/auth/register       6 requests    0 fails (100% success rate)    Avg: 224ms
POST /api/auth/login-client   5 requests    5 fails (403 Forbidden)*

* 403 ошибки ожидаемы - новые пользователи требуют верификации (is_verified=false)
```

## Внесенные изменения

### 1. Обновлен seeder
**Файл:** `app/seeders/user/user_seeder.py:32,51`
- Пароль admin: `admin123` → `Admin123!`
- Пароль client: `admin123` → `Client123!`

### 2. Добавлено поле IIN в регистрацию
**Файл:** `locustfile.py:94,97`
- Добавлено генерация 12-значного ИИН
- Добавлено поле `patronomic: None`

### 3. Исправлен формат телефона
**Файл:** `locustfile.py:93`
- Убран знак "+" из генерации телефона
- Теперь: `77XXXXXXXXX` вместо `+77XXXXXXXXX`

### 4. Обновлены пароли в тестах
**Файл:** `locustfile.py:182,344,435`
- Все пароли приведены к соответствию PASSWORD_REGEX

### 5. Создан скрипт обновления БД
**Файл:** `update_passwords.py`
- Скрипт для обновления паролей в существующей БД
- Уже выполнен: пароли в БД обновлены

## Актуальные учетные данные

### Администратор
```
username: admin
password: Admin123!
email: admin@example.com
phone: 77000000001
```

### Клиент
```
username: client
password: Client123!
email: client@example.com
phone: 77000000002
```

## Запуск Locust после исправлений

### Web UI режим
```bash
locust --host=http://localhost:8000
```

### Headless режим
```bash
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless
```

### Конкретный test case
```bash
# Тест авторизации
locust --host=http://localhost:8000 AuthUser

# Тест администратора
locust --host=http://localhost:8000 AdminOperationsUser

# Тест клиента с корзиной
locust --host=http://localhost:8000 ProductBrowserUser
```

## Проверка исправлений

### 1. Убедитесь что БД обновлена
```bash
python update_passwords.py
```

### 2. Запустите сервер
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Проверьте авторизацию вручную
```bash
curl -X POST "http://localhost:8000/api/auth/login-client" \
  -H "Content-Type: application/json" \
  -d '{"username":"client","password":"Client123!"}'
```

### 4. Запустите Locust тест
```bash
locust --host=http://localhost:8000 AuthUser --users 1 --spawn-rate 1 --run-time 10s --headless
```

## Валидация требований в проекте

### Расположение валидационных констант
- **Регулярные выражения:** `app/shared/validation_constants.py`
- **DTO константы:** `app/shared/dto_constants.py`
- **Field константы:** `app/shared/field_constants.py`

### Применение в DTOs
- **LoginDTO:** `app/adapters/dto/auth/login_dto.py`
- **RegisterDTO:** `app/adapters/dto/auth/register_dto.py`

### Бизнес-логика авторизации
- **Login use case:** `app/use_case/auth/login_case.py`
- **Login client use case:** `app/use_case/auth/login_client_case.py`

## Известные ограничения

### Верификация пользователей
После регистрации пользователи создаются с `is_verified=false` и требуют верификации. Это нормальное поведение для безопасности.

**Рекомендация для тестирования:**
- Используйте уже верифицированных пользователей (`admin`, `client`) для логина
- Или реализуйте отдельный эндпоинт для верификации пользователей в тестах

**Пример обхода для dev-среды:**
```python
# В AuthenticationFlow не пытаться логиниться сразу после регистрации
# Вместо этого использовать ProductBrowserUser или AdminOperationsUser
```

## Заключение

Все валидационные ошибки 422 устранены. Теперь:
1. ✅ Пароли соответствуют требованиям безопасности (PASSWORD_REGEX)
2. ✅ Телефоны в корректном формате (77XXXXXXXXX без +)
3. ✅ Поле IIN добавлено во все регистрации
4. ✅ БД обновлена с новыми паролями для admin/client
5. ✅ Locust тесты работают без 422 ошибок
6. ✅ Регистрация работает на 100%
7. ✅ Авторизация работает для верифицированных пользователей

При необходимости создания новых пользователей в тестах всегда используйте валидные данные согласно требованиям из `validation_constants.py`.
