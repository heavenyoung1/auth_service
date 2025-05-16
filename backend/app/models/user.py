from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Literal

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, info={"min_length": 6}) # Минимальная длина - 6 символов
    fullname: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Literal["admin", "user"]] = mapped_column(String, default="user")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    refresh_tokens =  relationship("RefreshToken", back_populates="User", cascade="all, delete")

    # Для отладки определяется метод repr
    def __repr__(self) -> str:
        return f"Метод __repr__: User(id={self.id!r}, login={self.login!r}, fullname={self.fullname!r})"

