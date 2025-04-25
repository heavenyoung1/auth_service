from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base(DeclarativeBase):
    pass

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER, nullable=False) #Enum(Role) можно удалить (далее), нужен для прозрачной работы с БД и валидации данных 

    # Для отладки определяется метод repr
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# Для тестов
user = User(id=1, name="Ivan", fullname="Ivan Petrov")

User.__tablename__
User.__mapper__
