from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"
    users: str = "/users"


    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.auth)
        path = "".join(parts)
        return path[:1]


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_prefix="APP_CONFIG__",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    access_token: AccessToken
    db: DataBaseConfig
    api: ApiPrefix = ApiPrefix()


settings = Settings()
