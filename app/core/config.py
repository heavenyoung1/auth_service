from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # --- Токены --- 
    SECRET_KEY: str = Field(description="Секретный ключ для JWT")
    ALGORITHM: str = Field(default="HS256", description="Алгоритм шифрования JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Время жизни access-токена в минутах")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, description="Время жизни refresh-токена в днях")

    # --- База данных --- 
    DATABASE_URL: str = Field(description="URL основной базы данных")
    TEST_DATABASE_URL: Optional[str] = Field(default=None, description="URL тестовой базы данных")

    # --- Параметры подключения к PostgreSQL ---
    PG_HOST: str = Field(description="Хост PostgreSQL")
    PG_DB: str = Field(description="Название базы данных")
    PG_PORT: str = Field(description="Порт подключения к базе данных")
    PG_USER: str = Field(description="Имя пользователя PostgreSQL")
    PG_PASSWORD: str = Field(description="Пароль PostgreSQL")

    # --- Конфигурация ---
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()