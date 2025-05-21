import psycopg2
from psycopg2 import OperationalError

from app.core.config import settings
from app.core.logger import logger

def test_connection():
    conn = None # Инициализация переменной
    try:
        conn = psycopg2.connect(
            host=settings.PG_HOST,
            database=settings.PG_DB,
            port=settings.PG_PORT,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
        )
        logger.info("✅ Успешное подключение к PostgreSQL!")
        
        # Проверяем версию PostgreSQL
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            logger.info(cursor.fetchone()[0])
            
        # Проверяем список баз данных
        with conn.cursor() as cursor:
            cursor.execute("SELECT datname FROM pg_database;")
            logger.info("\nСписок баз данных:")
            for db in cursor.fetchall():
                logger.info(f"- {db[0]}")
                
    except OperationalError as e:
        logger.error(f"❌ Ошибка подключения: {e}")
    finally:
        if conn:
            conn.close()

