from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated

class CreateUser(BaseModel):
    username: Annotated[str]
    email: EmailStr

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True) #Читай документацию Pydantic - Strict Mode (Жёсткий режим)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True