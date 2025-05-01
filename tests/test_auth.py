import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.user import Base
from app.database.db import get_session


TEST_DATABASE_URL = "postgresql+psycopg2://postgres:P%40ssw0rd@192.168.31.168:5432/auth_test_db"
engine = create_engine(TEST_DATABASE_URL, echo=True)
TestingSession = sessionmaker(engine)

@pytest.fixture(scope="function")
def setup_db():
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setupt_db):
    def override_get_session():
        with TestingSession() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()