from pydantic import BaseModel

class AccessToken(BaseModel):
    token_type: str
    access_token: str


class RefreshToken(AccessToken):
    refresh_token: str