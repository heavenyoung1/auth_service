from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class RefreshToken(Base):
    __tablename__ = "refreshToken"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True , nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime)

    user = relationship("User", back_populates="refreshToken")

    def __repr__(self):
        return f"RefreshToken id={self.id}, token={self.token[:9]}"