FROM python:3.11-slim

# Установка системных зависимостей для PostgreSQL и других пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директорий для логов и статических файлов  
RUN mkdir -p logs static uploads

# Открытие порта
EXPOSE 8000

# Создание скрипта запуска
RUN echo '#!/bin/bash\nalembic upgrade head\nuvicorn app.main:app --host 0.0.0.0 --port 8000' > /app/start.sh && \
    chmod +x /app/start.sh

# Команда запуска
CMD ["/app/start.sh"]