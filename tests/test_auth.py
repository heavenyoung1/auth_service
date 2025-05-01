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
def client(setup_db):
    def override_get_session():
        with TestingSession() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_register_success(client):
    response = client.post("/API/v0.1/register", json={
        "login": "testuser",
        "fullname": "Test User",
        "password": "password",
        "role": "user"
        }
    )
    print(response.text)  # Посмотреть сырой ответ
    print(response.json())  # Посмотреть распарсенный JSON
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_duplicate_login(client):
    client.post("/API/v0.1/register", json={
        "login": "testuser",
        "fullname": "Test User",
        "password": "password",
        "role": "user"
        }
    )

    response = client.post("/API/v0.1/register", json={
        "login": "testuser",
        "fullname": "Test User",
        "password": "password",
        "role": "user"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Такой логин уже существует."