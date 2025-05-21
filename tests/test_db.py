from app.models.user import User
from app.core.logger import logger

from tests.conftest import engine, test_session
from sqlalchemy import text


def test_sqlalchemy_connection(test_session):
    """ Тест - Подключентие к БД при помощи SQLAlchemy """
    assert test_session is not None
    logger.info("Успешное подключение к PostgreSQL через SQLAlchemy!")

    # Получение версии PostgreSQL
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version();")).scalar()
        logger.info(f"Версия PostgreSQL: {version}")

    # Получение списка баз данных
    result = test_session.execute(text("SELECT datname FROM pg_database;"))
    database = [row[0] for row in result]
    logger.info("Список баз данных")
    for db in database:
        logger.info(f"БД: {db}")

def test_create_user(test_session):
    """ Тест - создание тестового пользователя """
    user = User(
        login="testlogin",
        fullname="Test User",
        hashed_password="password",
        role="user",
    )

    # Сохранение в БД
    test_session.add(user)
    test_session.commit()

    # Проверка создания пользователя (что он был создан)
    db_user = test_session.query(User).filter(User.login == "testlogin").first()
    assert db_user is not None, "Пользователь не был создан"
    assert db_user.login == "testlogin"
    logger.info(f"Метод __repr__: {db_user}")
