import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.database.db import engine, get_session, init_db
from app.models.user import User, Role, Base

@pytest.fixture(scope="function")
def setup_db():
    init_db()  # Создаем таблицы
    yield
    Base.metadata.drop_all(bind=engine)  # Удаляем после теста

def test_sqlalchemy_connection(setup_db):
    with engine.connect() as connection:
        assert connection is not None, "Не удалось подключиться к базе данных"
        print("✅ Успешное подключение к PostgreSQL через SQLAlchemy!")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"PostgreSQL version: {version}")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database;"))
        databases = [row[0] for row in result]
        print("\nСписок баз данных:")
        for db in databases:
            print(f"- {db}")

def test_create_user(setup_db):
    with next(get_session()) as session:
        user = User(login="testlogin", fullname="Test User", hashed_password="hashed", role=Role.USER)
        session.add(user)
        session.commit()
        db_user = session.query(User).filter(User.login == "testlogin").first()
        assert db_user is not None, "Пользователь не был создан"
        assert db_user.login == "testlogin"
        print(f"Метод __repr__: {db_user}")