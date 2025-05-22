from app.core.config import settings
from app.core.logger import logger
from app.models.token import RefreshToken
from app.models.user import User

from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from dataclasses import dataclass
from jose import jwt
import pytest
from sqlalchemy.sql import text
from unittest.mock import patch, MagicMock


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

def test_register_success(client, user_factory): # TEST PASSED
    """Тест - успешная регистрация пользователя"""
    user = user_factory()  # Создание данных пользователя из класса UserData
    response = client.post("/API/v0.1/register", json=user.__dict__)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_duplicate_login(client, user_factory): # TEST PASSED
    """Тест - попытка регистрации с уже существующим логином"""
    user = user_factory() # Создание данных пользователя из класса UserData
    client.post("/API/v0.1/register", json=user.__dict__)

    # Попытка повторной регистрации с тем же логином
    response = client.post("/API/v0.1/register", json=user.__dict__)

    assert response.status_code == 400
    assert response.json()["detail"] == "Такой логин уже существует"

def test_register_short_password(client, user_factory): # TEST PASSED
    """Тест - попытка регистрации с коротким паролем"""
    user = user_factory(password="000")  # Создание данных пользователя из класса UserData c переопределением пароля
    response = client.post("/API/v0.1/register", json=user.__dict__) 

    assert response.status_code == 422, "Ошибка 422, выдаётся Pydantic`ом, валидация происходит в схеме UserCreate"

def test_login_success(client, user_factory): # TEST PASSED
    """Тест - Успешный вход"""
    user = user_factory()  # Создание данных пользователя из класса UserData
    # Регистрация пользователя 
    client.post("/API/v0.1/register", json=user.__dict__) 
    
    # Логин пользователя
    response = client.post("/API/v0.1/login", data={
        "username": "testUser",
        "password": "password"
        }
    )
    response_data = response.json()
    logger.debug(f"Access token: {response_data['access_token']}")
    logger.debug(f"Refresh token: {response_data['refresh_token']}")
    logger.debug(f"Full response: {response_data}")

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_wrong_password(client, user_factory): # TEST PASSED
    """Тест - Логин с неправильным паролем"""
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

def test_login_unexistent_user(client): # TEST PASSED
    """Тест - Логин несуществующего пользователя (неверный логин)"""    
    response = client.post("/API/v0.1/login", data={
        "username": "testUser111",
        "password": "PASSWORD"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин"

def test_get_current_user(client, user_factory): # TEST PASSED
    """Тест - получение текущего пользователя"""
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

def test_refresh_token_success(client, user_factory):
    """Тест - обновление access-token успешно"""
    user = user_factory()  # Создание данных пользователя из класса UserData

    client.post("/API/v0.1/register", json=user.__dict__)

    # Логин пользователя
    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/API/v0.1/refresh", json={"refresh_token": refresh_token})
    response_data = response.json()

    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Response body: {response_data}")

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"


def test_get_current_user_invalid_token(client):
    """Тест - получение текущего пользователя с некорректным access-token"""
    response = client.get("/API/v0.1/me", headers={"Authorization": f"Bearer invalidddd_token"})
    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Response body: {response.json()}")
    assert response.status_code == 401

def test_get_current_user_missing_sub(client):
    """Тест - отработка нарушенной структуры токена"""

    # Создаём токен без "sub"
    token = jwt.encode({}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    response = client.get("/API/v0.1/me", headers={"Authorization": f"Bearer {token}"})
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["detail"] == "Не удалось подтвердить учетные данные (credentials_exception)"

def test_user_not_found(client):
    """Тест - отработка некорретных sub"""
    token = jwt.encode({"sub": "nonexist_user"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    response = client.get("/API/v0.1/me", headers={"Authorization": f"Bearer {token}"})
    response_data = response.json()
    
    assert response.status_code == 401
    assert response_data["detail"] == "Не удалось подтвердить учетные данные (credentials_exception)"

def test_error_creating_refresh_token(client, user_factory):
    """Тест - ошибка создания refresh_token """
    user = user_factory()  # Создание данных пользователя из класса UserData

    client.post("/API/v0.1/register", json=user.__dict__)

    # Мокирование create_refresh_token для возврата None
    with patch("app.api.v1.auth.create_refresh_token", return_value=None) as mock_refresh:
        # Логин пользователя
        login_response = client.post("/API/v0.1/login", data={
            "username": user.login,
            "password": user.password
            }
        )
        logger.info(f"Mock called: {mock_refresh.called}")
        assert login_response.status_code == 500
        login_json = login_response.json()
        assert login_json["detail"] == "Ошибка создания refresh-token!"
        logger.info(login_json)

def test_refresh_token_not_found(client, user_factory):
    """Тест - Refresh-token не найден"""
    user = user_factory() 
    client.post("/API/v0.1/register", json=user.__dict__)
    client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )
    refresh_response = client.post("/API/v0.1/refresh", json={
        "refresh_token": "QWERTY12345",
        }
    )
    assert refresh_response.status_code == 404
    assert refresh_response.json()["detail"] == "Refresh-токен не найден"

def test_token_lifetime(client, user_factory, test_session):
    """Тест - проверка жизни токена """
    user = user_factory()
    client.post("/API/v0.1/register", json=user.__dict__)
    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )
    refresh_token = login_response.json().get("refresh_token")
    db_token = test_session.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    future_time = db_token.expires_at + timedelta(seconds=1)
    with patch("app.api.v1.auth.datetime") as mock_datetime:
        mock_datetime.now.return_value = future_time
        mock_datetime.timezone.utc = timezone.utc

        refresh_response = client.post("/API/v0.1/refresh", json={
            "refresh_token": refresh_token,
            }
        )
    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Refresh-токен истек"

def test_error_refresh_token(client, user_factory, test_session):
    """Тест - Проверка обработки ошибки при обновлении refresh-токена """
    user = user_factory()
    client.post("/API/v0.1/register", json=user.__dict__)
    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )
    refresh_token = login_response.json().get("refresh_token")

    with patch("app.api.v1.auth.create_refresh_token", side_effect=ValueError("Ошибка генерации токена")) as mock_create:
        refresh_response = client.post("/API/v0.1/refresh", json={"refresh_token": refresh_token})
        assert refresh_response.status_code == 500, f"Ожидался код 500, получен {refresh_response.status_code}"
        detail = refresh_response.json().get("detail")
        assert detail == "Ошибка при обновлении токена", \
            f"Ожидалось сообщение 'Ошибка при обновлении токена', получено: {detail}"
        assert mock_create.called, "create_refresh_token не был вызван"

    logger.info("Тест обработки ошибки при обновлении refresh-токена успешен") 

def test_logout_user(client, user_factory):
    """Тест - выход пользователя из сессии """
    user = user_factory()
    client.post("/API/v0.1/register", json=user.__dict__)

    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
        }
    )
    login_response_data = login_response.json()
    access_token = login_response_data["access_token"]
    refresh_token = login_response_data["refresh_token"]
    response = client.post("/API/v0.1/logout", 
                           json={"refresh_token": refresh_token},
                           headers={"Authorization": f"Bearer {access_token}"}
                           )
    
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json["detail"] == "Успешный выход"

def test_refresh_token_not_found(client, user_factory):
    """Тест - Проверка ошибки, если refresh-токен не найден при выходе."""
    user = user_factory()
    client.post("/API/v0.1/register", json=user.__dict__)
    login_response = client.post("/API/v0.1/login", data={
        "username": user.login,
        "password": user.password
    })
    assert login_response.status_code == 200, "Логин не удался"

    refresh_response = client.post("/API/v0.1/refresh", json={
        "refresh_token": "not_a_real_token"
    })
    assert refresh_response.status_code == 404
    assert refresh_response.json()["detail"] == "Refresh-токен не найден"
