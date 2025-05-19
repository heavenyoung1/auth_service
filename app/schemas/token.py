from pydantic import BaseModel

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(AccessToken):
    refresh_token: str