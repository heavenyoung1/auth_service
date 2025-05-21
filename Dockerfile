# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем UV
RUN pip install uv

# Копируем pyproject.toml и другие файлы для установки зависимостей
COPY pyproject.toml .

# Устанавливаем ВСЕ зависимости (основные + dev)
RUN uv sync --all-extras

# Копируем весь исходный код backend (без вложенной папки backend/)
COPY . .

# Настраиваем автоматическую активацию виртуальной среды
RUN echo "source /app/.venv/bin/activate" >> /root/.bashrc

# Добавление рабочей директории
ENV PYTHONPATH=/app

# Указываем порт, который будет использоваться
EXPOSE 8000

# Запускаем тесты при сборке (опционально)
RUN pytest tests -v --log-cli-level=INFO

# Запускаем FastAPI с помощью Uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]