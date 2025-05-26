from app.main import app
from app.models.user import Base
from app.database.db import get_session
from app.core.config import settings

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Настройка тестовой Базы Данных
engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
TestingSession = sessionmaker(engine)

@pytest.fixture(scope="function")
def setup_db():
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_session(setup_db):
    with TestingSession() as session:
        yield session

@pytest.fixture
def client(setup_db):
    def override_get_session():
        with TestingSession() as session:
            yield session

    # Подменяем зависимость для тестов
    app.dependency_overrides[get_session] = override_get_session

    # Создаем тестовый клиент
    with TestClient(app) as client:
        yield client

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()

# Настройки подключения к PostgreSQL
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "P@ssw0rd"
POSTGRES_HOST = "10.165.1.63"
POSTGRES_PORT = "5432"
ADMIN_DB = "postgres"

# @pytest.fixture(scope="session")
# def admin_connection():
#     connection = psycopg2.connect(
#         dbname=ADMIN_DB,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT,    
#     )
#     connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     yield connection
#     connection.close()

# Фикстура для подключения к конкретной базе
@pytest.fixture
def db_connection(request):
    """Фикстура для подключения к указанной базе данных."""
    db_name = request.param
    connection = psycopg2.connect(
        dbname=db_name,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    yield connection, db_name
    connection.close()