import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        conn = psycopg2.connect(
            host="192.168.31.168",
            port="5432",
            user="postgres",
            password="P@ssw0rd",
            database="auth_db"
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