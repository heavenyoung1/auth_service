from app.core.config import settings
from app.core.security import pwd_context, verify_password, create_access_token

import pytest
from jose import jwt
from typing import Literal
from datetime import datetime, timezone, timedelta

# Фикстура pytest - для переиспользования тестовых данных
@pytest.fixture
def test_password():
    return "test_password"

@pytest.fixture
def test_data():
    return {
        "sub": "001001",
        "role": "user",
        "exp": 1709840800,
        "iat": 1709837200
    }

def test_verify_password_success(test_password: Literal['test_password']):
    """ Тест - проверка корректного хеширования пароля """
    hashed_password = pwd_context.hash(test_password)
    assert verify_password(test_password, hashed_password) is True

def test_verify_password_failure(test_password: Literal['test_password']):
    """ Тест - проверка некорректного ввода пароля """
    hashed_password = pwd_context.hash(test_password)
    assert verify_password("wrong_password", hashed_password) is False

def test_verify_password_empty(test_password: Literal['test_password']):
    """ Тест - проверка ввода пустого пароля"""
    hashed_password = pwd_context.hash(test_password)
    assert verify_password("", hashed_password) is False

def test_create_access_token(test_data: dict):
    """ Тест - Создание Access-Token"""
    token = create_access_token(test_data)

    assert isinstance(token, str), "Токен должен быть строкой"
    assert len(token.split(".")) == 3, "Неверный формат JWT (должно быть 3 части)"

    # Декодирование токена для проверки содержимого
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "001001", "sub должен совпадать"
    assert decoded["role"] == "user", "role должен совпадать"
    assert "exp" in decoded, "Токен должен содержать срок действия"
    assert "iat" in decoded, "Токен должен содержать момент создания"

def test_token_expiration(test_data: dict):
    """ Тест - проверка корректного времени действия токена """
    token = create_access_token(test_data)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Переменные для exp (время окончения действия токена)
    excepted_exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    assert abs((excepted_exp - actual_exp).total_seconds()) < 5, "Неверный срок действия токена"






