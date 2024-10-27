from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class AccessToken(BaseModel):
    lifetime_seconds: int = 3600

class DataBaseConfig(BaseModel):
    url: PostgresDsn

class Settings(BaseSettings):
    access_token: AccessToken = AccessToken()
    db: DataBaseConfig = DataBaseConfig()



settings = Settings()
