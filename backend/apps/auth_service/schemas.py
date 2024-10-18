import uuid
from pydantic import BaseModel
from fastapi_users import schemas

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(schemas.BaseUserUpdate):
    pass