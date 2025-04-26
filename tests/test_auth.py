import pytest
from app.core.security import pwd_context, verify_password

# Проверка пароля - успешная
def test_verify_password_success():
    # 1. Хешируем тестовый пароль
    hashed_password = pwd_context.hash("test_password")

    # 2. Проверяем, что функция возвращает True для верного пароля
    assert verify_password("test_password", hashed_password) is True

def test_verify_password_failure():
    # 1. Хешируем тестовый пароль
    hashed_password = pwd_context.hash("test_password")

    # 2. Проверяем, что функция возвращает False для неверного пароля
    assert verify_password("wrong_password", hashed_password) is False