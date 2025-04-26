import pytest
from app.core.security import pwd_context, verify_password

# Фикстура pytest - для переиспользования тестовых данных
@pytest.fixture
def test_password():
    return "test_password"

# Проверка пароля - успешная
def test_verify_password_success(test_password):
    # Хешируем тестовый пароль
    hashed_password = pwd_context.hash(test_password)

    # Проверяем, что функция возвращает True для верного пароля
    assert verify_password(test_password, hashed_password) is True

# Проверка пароля - НЕуспешная
def test_verify_password_failure(test_password):
    # Хешируем тестовый пароль
    hashed_password = pwd_context.hash(test_password)

    # Проверяем, что функция возвращает False для неверного пароля
    assert verify_password("wrong_password", hashed_password) is False

# Проверка пустого пароля
def test_verify_password_empty(test_password):
    # Хешируем тестовый пароль
    hashed_password = pwd_context.hash(test_password)

    assert verify_password("", hashed_password) is False

# ---------------- ТЕСТЫ ДЛЯ ТОКЕНА ---------------- #
