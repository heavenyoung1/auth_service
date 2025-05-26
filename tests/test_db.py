from app.models.user import User
from app.core.logger import logger

from sqlalchemy import text
import pytest

@pytest.mark.usefixtures("test_session")
def test_create_user(test_session):
    """ Тест - создание тестового пользователя, вручную """
    user = User(
        login="testlogin",
        fullname="Test User",
        hashed_password="password",
        role="user",
    )

    test_session.add(user)
    test_session.commit()
    logger.info(f"Пользователь {user.login} добавлен в базу.")

    # Проверка создания пользователя (что он был создан)
    db_user = test_session.query(User).filter(User.login == "testlogin").first()
    logger.info(f"Метод __repr__: {db_user}")

    assert db_user is not None, "Пользователь не был создан"
    assert db_user.login == "testlogin", "Логин пользователя не совпадает"
    assert db_user.fullname == "Test User", "Имя пользователя не совпадает"
    assert db_user.role == "user", "Роль пользователя не совпадает"

