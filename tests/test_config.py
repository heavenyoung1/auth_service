import pytest
from app.core.config import settings

def test_config():
    assert settings.DATABASE_URL is not None, "DATABASE_URL должен быть задан"
    assert settings.SECRET_KEY is not None, "SECRET_KEY должен быть задан"
    assert settings.ALGORITHM == "HS256", "ALGORITHM должен быть HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES != 0 and settings.ACCESS_TOKEN_EXPIRE_MINUTES is not None, "ACCESS_TOKEN_EXPIRE_MINUTES не должен быть равен 0"

    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"SECRET_KEY: {settings.SECRET_KEY[:4]}... (скрыто для безопасности)")
    print(f"ALGORITHM: {settings.ALGORITHM}")
    print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")