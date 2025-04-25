from pydantic import BaseModel, Field
from app.models.user import Role

class UserBase(BaseModel):
    login: str
    fullname: str

class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=32)
    role: Role

class UserReturn(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True

print(Role.ADMIN)
# python -m app.schemas.user - команда для тестирования работы модуля как пакета