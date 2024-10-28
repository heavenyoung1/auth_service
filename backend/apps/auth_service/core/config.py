from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


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
    env_prefix = "APP_CONFIG__"
    api: ApiPrefix = ApiPrefix()


settings = Settings()
