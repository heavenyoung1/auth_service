from app.main import app
from app.models.user import Base
from app.database.db import get_session
from app.core.config import settings
from app.core.logger import logger

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

# Настройка тестовой Базы Данных
engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
TestingSession = sessionmaker(engine)

@pytest.fixture(scope="function")
def setup_db():
    """ Инициализирует тестовую базу данных перед тестом и очищает данные после  """
    logger.info("Инициализация тестовой базы данных...")
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)
    # Подключаемся к базе для очистки данных

@pytest.fixture
def test_session(setup_db):
    """ Предоставляет сессию SQLAlchemy для тестов """
    with TestingSession() as session:
        yield session

@pytest.fixture
def client(setup_db):
    """ Предоставляет тестовый клиент FastAPI с переопределённой сессией """
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
    logger.info("Тестовый клиент FastAPI закрыт.")
