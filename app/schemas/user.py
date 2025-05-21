from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class UserBase(BaseModel):
    login: str = Field(
        min_length=6, 
        max_length=32,
        json_schema_extra={
            "example": "qwerty",
            "description": "Логин должен быть от 6 до 32 символов"
            }
        )
    fullname: str = Field(example="Уилл Смитт")


class UserCreate(UserBase):
    password: str = Field(
        min_length=4, 
        max_length=32,
        json_schema_extra={
            "example": "myp@ssword123",
            "description": "Пароль должен быть от 4 до 32 символов"
            }
    )
    role: Literal["admin", "user"]


class UserReturn(UserBase):
    id: int
    role: Literal["admin", "user"]

    model_config = ConfigDict(from_attributes=True)

