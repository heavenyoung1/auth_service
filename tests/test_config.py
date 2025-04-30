from app.core.config import settings

def test_config():
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    assert settings.DATABASE_URL == "postgresql+psycopg2://postgres:P@ssw0rd@192.168.31.168:5432/auth_db"

if __name__ == "__main__":
    test_config()