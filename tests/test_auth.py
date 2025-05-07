from app.main import app
from app.models.user import Base
from app.database.db import get_session
from app.core.config import settings

from dataclasses import dataclass
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import pytest

import logging

logger = logging.getLogger(__name__)

# Если в коде есть print, используй чтобы вывести Debug Response >>> pytest tests\test_auth.py -v -s
# Настройка тестовой Базы Данных
engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
TestingSession = sessionmaker(engine)

@pytest.fixture(scope="function")
def setup_db():
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)

# Фабрика для генерации данных пользователя
@dataclass
class UserData:
    login: str = "testUser"
    fullname: str = "Test User"
    password: str = "password"
    role: str = "user"

@pytest.fixture
def user_factory():
    def create_user(**kwargs):
        return UserData(**kwargs)
    return create_user

@pytest.fixture
def client(setup_db):
    def override_get_session():
        with TestingSession() as session:
            yield session

    # Подменяем зависимость для тестов
    app.dependency_overrides[get_session] = override_get_session

    # Создаем тестовый клиент
    with TestClient(app) as client:
        yield client

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()

# Тест успешной регистрации пользователя
def test_register_success(client, user_factory):
    user = user_factory()  # Создание данных пользователя из класса UserData
    response = client.post("/API/v0.1/register", json=user.__dict__)
    assert response.status_code == 200
    assert "access_token" in response.json()

# Тест попытки регистрации с уже существующим логином
def test_register_duplicate_login(client, user_factory):
    user = user_factory() # Создание данных пользователя из класса UserData
    client.post("/API/v0.1/register", json=user.__dict__)

    # Попытка повторной регистрации с тем же логином
    response = client.post("/API/v0.1/register", json=user.__dict__)

    assert response.status_code == 400
    assert response.json()["detail"] == "Такой логин уже существует."

# Тест валидации короткого пароля (менее 4 символов)
def test_register_short_password(client, user_factory):
    user = user_factory(password="000")  # Создание данных пользователя из класса UserData c переопределением пароля
    response = client.post("/API/v0.1/register", json=user.__dict__) 

    assert response.status_code == 422, "Ошибка 422, выдаётся Pydantic`ом, валидация происходит в схеме UserCreate"

# Тест успешного входа
def test_login_success(client, user_factory):
    user = user_factory()  # Создание данных пользователя из класса UserData
    # Регистрация пользователя 
    client.post("/API/v0.1/register", json=user.__dict__) 
    
    # Логин пользователя
    response = client.post("/API/v0.1/login", data={
        "username": "testUser",
        "password": "password"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, user_factory):
    user = user_factory()  # Создание данных пользователя из класса UserData
    # Регистрация пользователя 
    client.post("/API/v0.1/register", json=user.__dict__) 

    # Логин пользователя c неправильным паролем
    response = client.post("/API/v0.1/login", data={
        "username": "testUser",
        "password": "PASSWORD"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный пароль"

def test_login_unexistent_user(client):
    response = client.post("/API/v0.1/login", data={
        "username": "testUser111",
        "password": "PASSWORD"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин"

# Тест - получение текущего пользователя
def test_get_current_user(client, user_factory):
    user = user_factory()  # Создание данных пользователя из класса UserData

    # Регистрация пользователя 
    register_response = client.post("/API/v0.1/register", json=user.__dict__)
    assert register_response.status_code == 200, f"Регистрация не удалась"

    # Логин пользователя
    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )
    login_response.status_code == 200, f"Логин не удался"
    token = login_response.json()["access_token"]

    # Запрос данные текущего пользователя
    response = client.get("/API/v0.1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_get_current_user_invalid_token(client):
    response = client.get("/API/v0.1/me", headers={"Authorization": f"Bearer invalidddd_token"})
    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Response body: {response.json()}")
    assert response.status_code == 401


