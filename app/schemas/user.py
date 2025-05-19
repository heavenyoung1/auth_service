from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

# python -m app.schemas.user - команда для тестирования работы модуля как пакета

class UserBase(BaseModel):
    login: str = Field(
        min_length=6, 
        max_length=32,
        json_schema_extra={
            "example": "qwerty",
            "description": "Логин должен быть от 6 до 32 символов"
            }
        )
    fullname: str

class UserCreate(UserBase):
    password: str = Field(
        min_length=4, 
        max_length=32)
    role: Literal["admin", "user"] # Ограничение значений

class UserReturn(UserBase):
    id: int
    role: Literal["admin", "user"] # Ограничение значений

    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str

