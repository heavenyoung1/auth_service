[![CI Pipeline](https://github.com/heavenyoung1/auth_service/actions/workflows/ci.yml/badge.svg)](https://github.com/heavenyoung1/auth_service/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Auth Service - Сервис аутентификации

Сервис аутентификации на основе FastAPI с JWT, SQLAlchemy и PostgreSQL. Поддерживает регистрацию пользователей, вход в систему и защищенные маршруты типа `/me`. Включает тесты с pytest и поддержку Docker для легкого развертывания.

## Особенности

- **Регистрация пользователей**: Создание новых пользователей с помощью `/API/v0.1/register`.
- **Вход пользователей**: Аутентификация пользователей и получение JWT-токенов с помощью `/API/v0.1/login`.
- **Защищенные маршруты**: Доступ к данным пользователя с помощью `/API/v0.1/me` с использованием JWT.
- **Доступ на основе ролей**: Поддерживает роли `user` и `admin` (с возможностью расширения до `/admin-only`).
- **Тесты**: Полный набор тестов с `pytest`.
- **Поддержка докеров**: Готовность к контейнерному развертыванию.

## Технологический стек

- **FastAPI**: Высокопроизводительный веб-фреймворк для создания API.
- **SQLAlchemy**: ORM для базы данных PostgreSQL.
- **PostgreSQL**: База данных для хранения пользовательских данных.
- **JWT**: Безопасная аутентификация на основе токенов.
- **Pytest**: Фреймворк для тестирования модульных тестов.

# Сборка приложения при помощи Docker-compose

### Установка и запуск docker-compose 
Важно! Устанавливать docker-compose через `curl`, из GitHub. Данного пакета нет в apt. Команда для установки ниже, актуальная версия на данный момент 2.36.0
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.36.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```
Для удобства в `docker-compose` добавлен `Portainer`, при помощи которого можно удобно управлять контейнерами, просматривать логи через графический интерфейс. Он стартует при сборке докера и доступен по адресу `https://localhost:9443`.

### Сборка проекта
```
docker-compose up --build -d
```

# Ручная сборка проекта на OC Linux Ubintu

### Обновление системы
```
sudo apt update && sudo apt upgrade -y
```

### Установка Python с необходимыми пакетами
```
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

### Установка curl, необходимого для менеджера пакетов uv
```
sudo apt install curl
curl --version
```

### Установка UV - менеджера управления зависимостями
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Перейдите в директорию, куда вы хотите клонировать репозиторий

### Клонирование репозитория
```
git clone https://github.com/heavenyoung1/auth_service.git
```

Важно! Переоткройте терминал и продолжите выполнение, открыв клонированный репозиторий и перейдя в папку `/backend/` следующей командой
```
cd /ваш_путь/auth_service/backend
```

### Создание виртуального окружения при помощи UV и его активация
```
uv venv
source .venv/bin/activate
```
### Установка зависимостей из файла pyproject.toml
```
uv sync
```

### Настройка файла окружения (.env)
Для работы проекта необходимо настроить переменные окружения, которые используются для подключения к базе данных и других конфигураций. Эти переменные хранятся в файле .env, который должен быть создан в папке `auth_service/backend/`.
1. Перейдите в директорию проекта:
```
cd auth_service/backend/
```
2. Создайте файл `.env`:
```
touch .env
```
3. Откройте файл .env в текстовом редакторе (например, `nano`):
```
nano .env
```
4. Добавьте в файл следующие переменные окружения, заменив значения на ваши данные:
```
!!! Для docker-compose вместо <host> прописать название сервера, в данном случае db

# URL для подключения к основной базе данных
DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>:<port>/<database_name>"

# URL для подключения к тестовой базе данных
TEST_DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>:<port>/<test_database_name>"

# Секретный ключ для подписи JWT-токенов
SECRET_KEY=<your-secret-key>

# Параметры подключения к PostgreSQL
PG_HOST="<database-host>"
PG_DB="<database-name>"
PG_PORT="<port>"
PG_USER="<username>"
PG_PASSWORD="<password>"
```
5. Cохраните файл и закройте редактор нажмите `Ctrl + O`, затем `Enter`

### Пример заполнения файла .env

```
# URL для подключения к основной базе данных
DATABASE_URL="postgresql+psycopg2://dbuser:securepass123@192.168.1.100:5432/main_db"

# URL для подключения к тестовой базе данных
TEST_DATABASE_URL="postgresql+psycopg2://dbuser:securepass123@192.168.1.100:5432/test_db"

# Секретный ключ для подписи JWT-токенов
SECRET_KEY=my-super-secret-key-987654321

# Параметры подключения к PostgreSQL
PG_HOST="192.168.1.100"
PG_DB="main_db"
PG_PORT="5432"
PG_USER="dbuser"
PG_PASSWORD="securepass123"
```

## Работа с Docker

### Создание Docker сети
```
docker network create auth-network
```

### Настройка и запуск контейнера PostgreSQL
```
docker run -d \
  --name auth-postgres \
  --network auth-network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secretpass123 \
  -e POSTGRES_DB=auth_db \
  -p 5432:5432 \
  postgres:latest
```

### Настройка и запуск контейнера PgAdmin
```
docker run -d \
  --name pgadmin \
  --network auth-network \
  -e PGADMIN_DEFAULT_EMAIL=admin@example.com \
  -e PGADMIN_DEFAULT_PASSWORD=adminpass123 \
  -p 8080:80 \
  dpage/pgadmin4
```

### Проверка создания контейнеров
```
docker ps
```

### Запуск скрипта для создания БД
```
python -m app.database.create_db
```

### Запуск тестов
```
pytest tests -v
```

### Запустите Uvicorn с явным указанием хоста 
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
`--host 0.0.0.0` разрешает подключения со всех интерфейсов

`--port 8000` явное указание порта