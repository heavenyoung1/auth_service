from psycopg2 import  connect, Error

from app.core.config import settings
from app.core.logger import logger

def create_database():
    connection = None # Инициализация переменной
    try:
        connection = connect(
            host=settings.PG_HOST,
            database="postgres",
            port=settings.PG_PORT,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
        )
        logger.info("✅ Успешное подключение к PostgreSQL!")

        connection.autocommit = True
        cursor = connection.cursor()

        # Проверка и создание базы данных
        databases = ["auth_test_db", "auth_db"]

        for i in databases:
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{i}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {i}")
                logger.info(f"База данных {i} успешно создана")
            else:
                logger.info(f"База данных {i} уже существует.")

    except Error as e:
        logger.info(f"❌ Ошибка при создании базы данных: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("Соединение закрыто.")

if __name__ == "__main__":
    create_database()