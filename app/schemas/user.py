from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class UserBase(BaseModel):
    login: str = Field(
        min_length=6, 
        max_length=32,
        )
    fullname: str 


class UserCreate(UserBase):
    password: str = Field(
        min_length=4, 
        max_length=32,
    )
    role: Literal["admin", "user"]


class UserReturn(UserBase):
    id: int
    role: Literal["admin", "user"]

    model_config = ConfigDict(from_attributes=True)

