Команда для запуска тестов (можно добавить еще один флаг -s для отображения всей информации, например print)
pytest tests\test_auth.py -v

запуск pytest-cov
# С подробным выводом непокрытых строк
pytest --cov=app --cov-report=term-missing tests/

## Работа с зависимостями

# Установка зависимости:
uv pip install fastapi sqlalchemy

# Сохранение в pyproject.toml и uv.lock:
uv pip install fastapi sqlalchemy --upgrade --sync --system

# Установка всего из pyproject.toml:
uv pip install --all --system