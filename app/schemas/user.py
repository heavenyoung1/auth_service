from pydantic import BaseModel, Field
from app.models.user import Role

# python -m app.schemas.user - команда для тестирования работы модуля как пакета

class UserBase(BaseModel):
    login: str
    fullname: str

class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=32)
    role: Role

class UserReturn(UserBase):
    id: int
    role: Role

    # для преобразования SQLAlchemy-объектов??????
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

