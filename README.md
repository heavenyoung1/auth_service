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

# Синхронизация виртуального окружения (Это установит все зависимости, указанные в uv.lock, в вашу виртуальную среду.)
uv sync


# Сервис авторизации
Ниже будет описана последовательность шагов для локального развертывания приложения на ОС Linux Ubuntu

### Обновление системы
```
sudo apt update && sudo apt upgrade -y
```

### Установка Python с необходимыми пакетами
```
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

### Установка UV - менеджера управления зависимостями
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

### Клонирование репозитория
```
git clone https://github.com/heavenyoung1/auth_service.git
cd your-fastapi-project 
```

### Установка виртуального окружения Python
``` 
sudo apt install python3.12-venv
```
### Создание виртуального окружения при помощи UV и его активация
```
uv venv
source .venv/bin/activate
```
### Установка UV в виртуальное окружение
```
pip install uv
```
