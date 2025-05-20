from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Literal, List

from app.models.base import Base
#from app.models.token import RefreshToken

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, info={"min_length": 6}) # Минимальная длина - 6 символов
    fullname: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Literal["admin", "user"]] = mapped_column(String, default="user")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    refresh_tokens: Mapped[List["RefreshToken"]] =  relationship(back_populates="user", cascade="all, delete") # Добавлен List, теперь связь - One To Many

    # Для отладки определяется метод repr
    def __repr__(self) -> str:
        return f"Метод __repr__: User(id={self.id!r}, login={self.login!r}, fullname={self.fullname!r})"

