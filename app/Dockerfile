# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY temp-requirements.txt .
RUN pip install --no-cache-dir -r temp-requirements.txt

# Копируем весь код бэкенда
COPY . .

# Запускаем FastAPI с помощью Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]