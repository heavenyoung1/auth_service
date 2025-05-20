from pydantic import BaseModel

class AccessTokenRequest(BaseModel):
    access_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class Auth2Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str