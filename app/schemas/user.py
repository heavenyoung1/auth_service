from pydantic import BaseModel, Field
from app.models.user import Role

# python -m app.schemas.user - команда для тестирования работы модуля как пакета

class UserBase(BaseModel):
    login: str = Field(min_length=6, max_length=32,
                       example="qwerty",
                       description=f"Логин должен быть от 6 до 32 символов")
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

# Тест создания пользователя
if __name__ == "__main__":
    user_create = UserCreate(login="testUser", fullname="Piter Parker", password="123456", role=Role.ADMIN)
    print(user_create)

# Тест валидации данных 
try:
    invalid_user = UserCreate(login="i", fullname="Test", password="123", role=Role.USER)
except ValueError as e:
    print(f"Ошибка валидации данных {e}")
