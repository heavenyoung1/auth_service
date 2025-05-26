import pytest
from dotenv import load_dotenv
import os
import psycopg2

from app.core.logger import logger
# Список баз данных для проверки
DATABASES = ["auth_db"]

# Ожидаемые таблицы
EXPECTED_TABLES = {"users", "refresh_tokens", "alembic_version"}

# Загружаем переменные из .env
load_dotenv()

# Константы подключения
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")

# Фикстура для подключения к базе
@pytest.fixture
def db_connection(request):
    """Фикстура для подключения к указанной базе данных."""
    db_name = request.param
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        yield connection, db_name
    except psycopg2.Error as e:
        pytest.fail(f"Не удалось подключиться к базе {db_name}: {e}")
    finally:
        connection.close()

@pytest.mark.parametrize("db_connection", DATABASES, indirect=True)
def test_table_exist(db_connection):
    """Проверяет наличие ожидаемых таблиц в указанной базе данных."""
    connection, db_name = db_connection
    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """)
        tables = {row[0] for row in cursor.fetchall()}
        logger.info(f"Найденные таблицы в базе {db_name}: {tables}")

        # Проверяем, что все ожидаемые таблицы присутствуют
        for table in EXPECTED_TABLES:
            assert table in tables, f"Таблица {table} отсутствует в базе {db_name}"
    finally:
        cursor.close()