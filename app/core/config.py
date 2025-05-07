from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None  # Добавляем опциональное поле
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PG_HOST: str
    PG_DB: str
    PG_PORT: str
    PG_USER: str
    PG_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()