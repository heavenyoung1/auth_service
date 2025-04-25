from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, info={"min_length": 6}) # Минимальная длина - 6 символов
    fullname: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.USER, nullable=False) #Enum(Role) можно удалить (далее), нужен для прозрачной работы с БД и валидации данных 

    # Для отладки определяется метод repr
    def __repr__(self) -> str:
        return f"Метод __repr__: User(id={self.id!r}, login={self.login!r}, fullname={self.fullname!r})"

# Для тестов
user = User(id=1, login="heavenyoung", fullname="Ivan Petrov")

#Для отладки вывод метода __repr__
print(user)

User.__tablename__
User.__mapper__

