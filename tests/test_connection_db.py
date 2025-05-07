import psycopg2
from psycopg2 import OperationalError

from app.core.config import settings

def test_connection():
    try:
        conn = psycopg2.connect(
            host=settings.PG_HOST,
            database=settings.PG_DB,
            port=settings.PG_PORT,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
        )
        print("✅ Успешное подключение к PostgreSQL!")
        
        # Проверяем версию PostgreSQL
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(cursor.fetchone()[0])
            
        # Проверяем список баз данных
        with conn.cursor() as cursor:
            cursor.execute("SELECT datname FROM pg_database;")
            print("\nСписок баз данных:")
            for db in cursor.fetchall():
                print(f"- {db[0]}")
                
    except OperationalError as e:
        print(f"❌ Ошибка подключения: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    test_connection()