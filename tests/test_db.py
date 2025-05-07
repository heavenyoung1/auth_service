from app.models.user import Base, User, Role
from app.core.config import settings

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Если возникают проблемы с неправильным чтением URL в терминале выполнить команду - удаление переменной окружения >>> Get-ChildItem Env:TEST_DATABASE_URL

# Используем тестовую БД
engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
Session = sessionmaker(engine)

# Функции для взаимодействия с тестовой БД
def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session() as session:
        yield session

@pytest.fixture(scope="function") # "function": Фикстура создается и уничтожается для каждого теста (функции).
def setup_db():
    init_db() # Создание таблиц
    yield()
    Base.metadata.drop_all(bind=engine) # Удаление таблиц

# Подключение к БД при помощи SQLAlchemy
def test_sqlalchemy_connection(setup_db: tuple[()]):
    with engine.connect() as connection:
        assert connection is not None
        print("Успешное подключение к PostgreSQL через SQLAlchemy!")

    # Получение версии PostgreSQL
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version();")).scalar() # Как вывести данные
        print(f"Версия PostgreSQL: {version}")

    # Получение списка баз данных
    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database;")) # pg_database — это системная таблица в PostgreSQL
        database = [row[0] for row in result]
        print("Список баз данных")
        for db in database:
            print(f"БД: {db}")

def test_create_user(setup_db: tuple[()]):
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
        db_user = session.query(User).filter(User.login == "testlogin").first()
        assert db_user is not None, "Пользователь не был создан"
        assert db_user.login == "testlogin"
        print(f"Метод __repr__: {db_user}")
