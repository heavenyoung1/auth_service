from pydantic import ValidationError
from app.schemas.user import UserCreate

# Тест создания пользователя
if __name__ == "__main__":
    user_create = UserCreate(login="testUser", fullname="Piter Parker", password="123456", role= "admin")
    print(user_create)

# Тест валидации данных 
try:
    invalid_user = UserCreate(login="i", fullname="Test", password="123", role="user")
except ValueError as e:
    print(f"Ошибка валидации данных {e}")

def test_user_create_valid():
    user = UserCreate(login="test@example.com", fullname="Test User", password="123456", role="user")
    assert user.login == "test@example.com"
    assert user.role == "user"

def test_user_create_invalid_password():
    try:
        UserCreate(login="test@example.com", fullname="Test User", password="12", role="user")
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True

# Команда для запуска тестов pytest tests/ -v 