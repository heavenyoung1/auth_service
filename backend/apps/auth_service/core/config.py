from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    access_token: AccessToken
    db: DataBaseConfig = DataBaseConfig
    api: ApiPrefix = ApiPrefix()

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_prefix="APP_CONFIG__",
    )


settings = Settings()
