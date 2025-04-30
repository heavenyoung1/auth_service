import pytest
from sqlalchemy import create_engine, text

from app.database.db import get_session, init_db
from app.models.user import Base, User, Role

# Используем тестовую БД
TEST_DATABASE_URL = "postgresql+psycopg2://postgres:P%40ssw0rd@192.168.31.168:5432/auth_test_db"
engine = create_engine(TEST_DATABASE_URL, echo=True) #

# "function": Фикстура создается и уничтожается для каждого теста (функции). Это значение по умолчанию и обеспечивает максимальную изоляцию тестов.

@pytest.fixture(scope="function") # Почему здесь описана scope="function", что это значит
def setup_db():
    init_db() # Создание таблиц
    yield() # Зачем здесь это?
    Base.metadata.drop_all(bind=engine)

# Подключение к БД при помощи SQLAlchemy
def test_sqlalchemy_connection(setup_db: tuple[()]):
    with engine.connect() as connection:
        assert connection is not None
        print("Успешное подключение к PostgreSQL через SQLAlchemy!")

    # Получение версии PostgreSQL
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();")) # Как вывести данные
        version = result.fetchone()[0]
        print(f"Версия PostgreSQL: {version}")

    # Получение списка баз данных
    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database;")) # что такое pg_database
        database = [row[0] for row in result]
        print("Список баз данных")
        for db in database:
            print(f"БД: {db}")

def test_create_user(setup_db):
    with next(get_session()) as session:
        # Создание тестового пользователя
        user = User(
            login="testlogin",
            fullname="Test User",
            hashed_password="password",
            role=Role.USER
        )

        # Сохранение в БД
        session.add(user)
        session.commit()

        # Проверка создания пользователя (что он был создан)
        db_user = session.query(User).filter(User.login == "testlogin").first() # Обязательно ли first()?
        assert db_user is not None, "Пользователь не был создан"
        assert db_user.login == "testlogin"
        print(f"Метод __repr__: {db_user}")
