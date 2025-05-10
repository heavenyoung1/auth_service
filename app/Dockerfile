# # Используем официальный образ Python
# FROM python:3.13-slim

# # Устанавливаем рабочую директорию
# WORKDIR /app

# # Копируем requirements.txt и устанавливаем зависимости
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Копируем весь код бэкенда
# COPY . .

# # Запускаем FastAPI с помощью Uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#-----------------------------------------------------------------------------

# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости (без dev-зависимостей)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Копируем весь код бэкенда
COPY . .

# Запускаем FastAPI с помощью Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]