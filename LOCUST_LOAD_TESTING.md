# 🚀 Locust Load Testing Guide

Это руководство по использованию Locust для нагрузочного тестирования Jankuier Backend API.

## 📋 Содержание

- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Доступные сценарии тестирования](#доступные-сценарии-тестирования)
- [Запуск тестов](#запуск-тестов)
- [Интерпретация результатов](#интерпретация-результатов)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 📦 Установка

### 1. Установка зависимостей

```bash
# Установка Locust и всех зависимостей
pip install -r requirements.txt

# Проверка установки
locust --version
```

### 2. Запуск приложения

Убедитесь, что ваше FastAPI приложение запущено:

```bash
# Запуск сервера (в отдельном терминале)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🎯 Быстрый старт

### Запуск с Web UI (рекомендуется)

```bash
# Базовый запуск с веб-интерфейсом
locust --host=http://localhost:8000

# Откройте браузер и перейдите на http://localhost:8089
```

В Web UI вы можете:
- Настроить количество пользователей (Number of users)
- Установить скорость появления пользователей (Spawn rate)
- Запустить/остановить тест
- Наблюдать метрики в реальном времени

### Запуск в headless режиме

```bash
# 100 пользователей, 10 пользователей в секунду, 60 секунд
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless

# С сохранением отчетов
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless \
       --html=reports/load_test_report.html \
       --csv=reports/load_test
```

## 🎭 Доступные сценарии тестирования

### 1. `PublicAPIUser` (вес: 3)

**Назначение**: Тестирование публичных API без аутентификации

**Эндпоинты**:
- `GET /api/city/all` - Список всех городов
- `GET /api/city/?page={page}` - Пагинация городов
- `GET /api/country/all` - Список стран
- `GET /api/sport/all` - Список видов спорта
- `GET /api/city/get/{id}` - Получение города по ID

**Использование**:
```bash
locust --host=http://localhost:8000 PublicAPIUser
```

### 2. `AuthUser` (вес: 2)

**Назначение**: Тестирование полного цикла аутентификации (регистрация → логин → профиль)

**Сценарий**:
1. Регистрация нового пользователя
2. Авторизация с полученными креденшилами
3. Получение данных профиля

**Использование**:
```bash
locust --host=http://localhost:8000 AuthUser --users 50 --spawn-rate 5
```

### 3. `ProductBrowserUser` (вес: 2)

**Назначение**: Симуляция пользователя, просматривающего товары

**Требования**: Аутентификация (использует тестового пользователя `client/client123`)

**Эндпоинты**:
- `GET /api/product/` - Просмотр товаров
- `GET /api/product/get/{id}` - Детали товара
- `GET /api/product-category/all` - Категории
- `GET /api/cart/my-cart` - Корзина пользователя

**Использование**:
```bash
locust --host=http://localhost:8000 ProductBrowserUser
```

### 4. `AcademyBrowserUser` (вес: 2)

**Назначение**: Тестирование работы с академиями и группами

**Эндпоинты**:
- `GET /api/academy/all` - Список академий
- `GET /api/academy/get/{id}` - Детали академии
- `GET /api/academy-group/` - Группы академий
- `GET /api/academy-group-schedule/all` - Расписание

**Использование**:
```bash
locust --host=http://localhost:8000 AcademyBrowserUser
```

### 5. `FieldBrowserUser` (вес: 2)

**Назначение**: Тестирование работы с полями и площадками

**Эндпоинты**:
- `GET /api/field/` - Список полей
- `GET /api/field/get/{id}` - Детали поля
- `GET /api/field-party/all` - Площадки
- `GET /api/field-party-schedule/all` - Расписание

**Использование**:
```bash
locust --host=http://localhost:8000 FieldBrowserUser
```

### 6. `AdminOperationsUser` (вес: 1)

**Назначение**: Тестирование административных операций

**Требования**: Аутентификация администратора (`admin/admin123`)

**Эндпоинты**:
- `GET /api/user/all` - Список пользователей
- `GET /api/role/all` - Роли
- `GET /api/permission/all` - Разрешения
- `GET /api/product-order-admin/` - Заказы (админ)

**Использование**:
```bash
locust --host=http://localhost:8000 AdminOperationsUser --users 10 --spawn-rate 1
```

### 7. `MixedOperationsUser` (вес: 4) ⭐ Рекомендуется

**Назначение**: Реалистичная симуляция реального пользователя

**Особенности**:
- Комбинирует различные типы запросов
- 30% вероятность аутентификации
- Смешанные веса для разных операций

**Использование**:
```bash
locust --host=http://localhost:8000 MixedOperationsUser --users 200 --spawn-rate 20
```

### 8. `StressTestUser` (вес: 1) ⚠️ Экстремальный

**Назначение**: Максимальная нагрузка для стресс-теста

**Предупреждение**: Использовать с осторожностью!

**Использование**:
```bash
locust --host=http://localhost:8000 StressTestUser --users 500 --spawn-rate 50 --run-time 30s
```

## 📊 Запуск тестов

### Рекомендуемые сценарии запуска

#### 1. Легкая нагрузка (smoke test)

```bash
locust --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 30s --headless
```

#### 2. Средняя нагрузка (обычный день)

```bash
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 5m --headless \
       --html=reports/medium_load.html
```

#### 3. Высокая нагрузка (пиковые часы)

```bash
locust --host=http://localhost:8000 --users 500 --spawn-rate 50 --run-time 10m --headless \
       --html=reports/high_load.html
```

#### 4. Стресс-тест (максимум)

```bash
locust --host=http://localhost:8000 StressTestUser --users 1000 --spawn-rate 100 --run-time 5m --headless \
       --html=reports/stress_test.html
```

#### 5. Комплексный тест (все сценарии)

```bash
# Запуск всех пользователей одновременно
locust --host=http://localhost:8000 --users 300 --spawn-rate 30 --run-time 10m --headless \
       --html=reports/full_test.html \
       --csv=reports/full_test
```

#### 6. Специфичный сценарий

```bash
# Только тестирование продуктов
locust --host=http://localhost:8000 ProductBrowserUser --users 150 --spawn-rate 15 --run-time 5m
```

### Настройка параметров

- `--users` (или `-u`): Общее количество симулируемых пользователей
- `--spawn-rate` (или `-r`): Скорость появления пользователей (пользователей/секунду)
- `--run-time` (или `-t`): Длительность теста (30s, 5m, 1h)
- `--headless`: Запуск без веб-интерфейса
- `--html`: Путь для сохранения HTML отчета
- `--csv`: Префикс для CSV файлов с результатами
- `--host`: URL тестируемого сервера

## 📈 Интерпретация результатов

### Основные метрики

#### Request metrics

- **Type**: Тип HTTP запроса (GET, POST, etc.)
- **Name**: Название эндпоинта
- **# Requests**: Общее количество запросов
- **# Fails**: Количество неудачных запросов
- **Median**: Медианное время ответа (ms)
- **Average**: Среднее время ответа (ms)
- **Min/Max**: Минимальное/максимальное время ответа (ms)
- **RPS**: Запросов в секунду (Requests Per Second)
- **Failures/s**: Ошибок в секунду

### Целевые показатели (SLA)

| Метрика | Хорошо | Приемлемо | Плохо |
|---------|--------|-----------|-------|
| **Average Response Time** | < 200ms | 200-500ms | > 500ms |
| **95th Percentile** | < 500ms | 500-1000ms | > 1000ms |
| **99th Percentile** | < 1000ms | 1000-2000ms | > 2000ms |
| **Error Rate** | < 0.1% | 0.1-1% | > 1% |
| **RPS (per server)** | > 100 | 50-100 | < 50 |

### Анализ результатов

#### ✅ Хорошие показатели
```
Type     Name                          # reqs      # fails  |    Avg     Min     Max  Median  |   req/s
GET      /api/city/all                   1523     0(0.00%)  |    142      87     456     140  |   50.77
GET      /api/product/ [browse]          1205     0(0.00%)  |    201     112     678     190  |   40.17
```

#### ⚠️ Проблемные показатели
```
Type     Name                          # reqs      # fails  |    Avg     Min     Max  Median  |   req/s
GET      /api/product/get/[id]           856    42(4.91%)  |    867     234    5432    1200  |   28.53
POST     /api/cart/add-item               234    15(6.41%)  |   1523     456    8765    1800  |    7.80
```

**Проблемы**:
- Высокий процент ошибок (> 1%)
- Большое среднее время ответа (> 500ms)
- Большой разброс между Min и Max (нестабильность)

## 🎯 Best Practices

### 1. Постепенное увеличение нагрузки

```bash
# Начните с малого
locust --host=http://localhost:8000 --users 10 --spawn-rate 1

# Постепенно увеличивайте
locust --host=http://localhost:8000 --users 50 --spawn-rate 5
locust --host=http://localhost:8000 --users 100 --spawn-rate 10
locust --host=http://localhost:8000 --users 500 --spawn-rate 50
```

### 2. Мониторинг сервера

Во время тестов мониторьте:
- **CPU usage**: `top` или `htop`
- **Memory usage**: `free -h`
- **Database connections**: PostgreSQL logs
- **Network**: `iftop` или `nethogs`

```bash
# В отдельном терминале
watch -n 1 'free -h && echo "---" && ps aux | grep uvicorn'
```

### 3. Тестирование в production-like окружении

- Используйте те же версии Python и библиотек
- Настройте базу данных аналогично production
- Включите все middleware и authentication
- Используйте gunicorn/uvicorn с workers

```bash
# Production-like запуск
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker \
         --bind 0.0.0.0:8000 --timeout 120
```

### 4. Создание реалистичных сценариев

- Используйте `MixedOperationsUser` для реальных паттернов
- Настройте правильные веса для разных операций
- Добавьте `wait_time` между запросами
- Симулируйте реальное поведение пользователей

### 5. Сохранение результатов

```bash
# Создайте директорию для отчетов
mkdir -p reports

# Запускайте тесты с сохранением результатов
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 5m --headless \
       --html=reports/test_$(date +%Y%m%d_%H%M%S).html \
       --csv=reports/test_$(date +%Y%m%d_%H%M%S)
```

## 🔧 Troubleshooting

### Проблема: Connection refused

**Решение**:
```bash
# Убедитесь, что сервер запущен
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Проверьте доступность
curl http://localhost:8000/docs
```

### Проблема: Высокий процент ошибок 401 Unauthorized

**Решение**:
- Проверьте credentials в `locustfile.py`
- Убедитесь, что seeders выполнены (`admin/admin123`, `client/client123`)
- Проверьте срок действия токенов

```bash
# Запустите seeders
python -c "import asyncio; from app.seeders.runner import run_seeders; asyncio.run(run_seeders())"
```

### Проблема: Timeout errors

**Решение**:
```python
# В locustfile.py увеличьте timeout
class MyUser(HttpUser):
    connection_timeout = 10.0  # default: 10.0
    network_timeout = 10.0     # default: 10.0
```

### Проблема: Database connection pool exhausted

**Решение**:
```python
# В app/infrastructure/db.py
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,          # Увеличьте pool_size
    max_overflow=40,       # Увеличьте max_overflow
)
```

### Проблема: Memory leak при длительных тестах

**Решение**:
- Используйте `--run-time` для ограничения длительности
- Мониторьте memory usage
- Перезапускайте сервер между тестами

```bash
# Ограничьте длительность
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 10m
```

## 📚 Дополнительные ресурсы

- [Официальная документация Locust](https://docs.locust.io/)
- [Best Practices for Load Testing](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- [Distributed Load Testing](https://docs.locust.io/en/stable/running-distributed.html)

## 🎓 Примеры команд для разных целей

### CI/CD Integration

```bash
# Быстрый smoke test для CI
locust --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 1m --headless --only-summary

# Exit code != 0 если есть ошибки
locust --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 2m --headless \
       --expect-workers 1 --exit-code-on-error 1
```

### Capacity Planning

```bash
# Найдите максимальную пропускную способность
# Постепенно увеличивайте users до появления ошибок

for users in 50 100 200 500 1000; do
  echo "Testing with $users users..."
  locust --host=http://localhost:8000 --users $users --spawn-rate 50 --run-time 2m --headless \
         --html=reports/capacity_${users}_users.html
  sleep 30  # Дайте серверу восстановиться
done
```

### Endurance Testing (длительный тест)

```bash
# 12-часовой тест для поиска memory leaks
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 12h --headless \
       --html=reports/endurance_test.html \
       --csv=reports/endurance_test
```

---

**Удачного тестирования! 🚀**
