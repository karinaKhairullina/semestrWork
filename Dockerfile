FROM python:3.9

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    nginx

# Установка инструментов тестирования
RUN pip install --no-cache-dir pytest mypy black

WORKDIR /app

# Копирование файлов проекта в образ Docker
COPY . .

# Установка зависимостей проекта
RUN pip install --no-cache-dir -r requirements.txt

# Установка pytest в образе Docker
RUN pytest --version
