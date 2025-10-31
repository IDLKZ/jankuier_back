# 🚀 Locust Quick Start

## Установка

```bash
pip install -r requirements.txt
```

## Базовые команды

### 1. Запуск с Web UI (самый простой способ)

```bash
locust --host=http://localhost:8000
```

Затем откройте браузер: `http://localhost:8089`

### 2. Быстрый smoke test (headless)

```bash
locust --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 30s --headless
```

### 3. Реалистичная нагрузка

```bash
locust --host=http://localhost:8000 MixedOperationsUser --users 100 --spawn-rate 10 --run-time 5m --headless
```

### 4. Стресс-тест

```bash
locust --host=http://localhost:8000 StressTestUser --users 500 --spawn-rate 50 --run-time 2m --headless
```

### 5. С сохранением отчета

```bash
mkdir -p reports
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 5m --headless \
       --html=reports/load_test.html \
       --csv=reports/load_test
```

## Доступные сценарии

| Сценарий | Описание | Вес |
|----------|----------|-----|
| `PublicAPIUser` | Публичные API (города, страны, спорт) | 3 |
| `AuthUser` | Регистрация + Логин + Профиль | 2 |
| `ProductBrowserUser` | Просмотр товаров и корзины | 2 |
| `AcademyBrowserUser` | Работа с академиями | 2 |
| `FieldBrowserUser` | Работа с полями | 2 |
| `AdminOperationsUser` | Административные операции | 1 |
| `MixedOperationsUser` | Реалистичная симуляция | 4 ⭐ |
| `StressTestUser` | Экстремальная нагрузка | 1 ⚠️ |

## Параметры

- `--users` или `-u`: Количество пользователей
- `--spawn-rate` или `-r`: Пользователей в секунду
- `--run-time` или `-t`: Длительность (30s, 5m, 1h)
- `--headless`: Без веб-интерфейса
- `--html`: Путь для HTML отчета
- `--csv`: Префикс для CSV файлов

## Целевые метрики

| Метрика | Хорошо | Приемлемо | Плохо |
|---------|--------|-----------|-------|
| Avg Response Time | < 200ms | 200-500ms | > 500ms |
| Error Rate | < 0.1% | 0.1-1% | > 1% |
| RPS | > 100 | 50-100 | < 50 |

## Troubleshooting

### Проблема: Connection refused
```bash
# Запустите сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Проблема: 401 Unauthorized
```bash
# Запустите seeders (создаст admin/client пользователей)
python -c "import asyncio; from app.seeders.runner import run_seeders; asyncio.run(run_seeders())"
```

---

Полная документация: [LOCUST_LOAD_TESTING.md](LOCUST_LOAD_TESTING.md)
