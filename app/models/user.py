from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    hashed_password = Mapped(String, nullable=False)

    # Для отладки определяется метод repr
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# Для тестов
user = User(id=1, name="Ivan", fullname="Ivan Petrov")

User.__tablename__
User.__mapper__
