from pydantic import BaseModel
from models.user import Role

class UserBase(BaseModel):
    login: str
    fullname: str

class UserCreate(UserBase):
    password: str
    role: Role


