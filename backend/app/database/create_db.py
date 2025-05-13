import psycopg2
from psycopg2 import Error

from app.core.config import settings


def create_database():
    conn = None # Инициализация переменной
    try:
        connection = psycopg2.connect(
            host=settings.PG_HOST,
            database=settings.PG_DB,
            port=settings.PG_PORT,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
        )
        print("✅ Успешное подключение к PostgreSQL!")

        connection.autocommit = True
        cursor = connection.cursor()

        # Проверка и создание базы данных
        databases = ["auth_test_db", "auth_db"]

        for i in databases:
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{i}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {i}")
                print(f"База данных {i} успешно создана.")
            else:
                print(f"База данных {i} уже существует.")

    except Error as e:
        print(f"Ошибка при создании базы данных: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто.")

if __name__ == "__main__":
    create_database()