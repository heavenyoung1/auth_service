from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, timedelta
from app.core.config import settings

from app.models.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    token: Mapped[str] = mapped_column(String, unique=True , nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

    def __repr__(self):
        return f"RefreshToken id={self.id}, token={self.token[:9]}"
    
    # @classmethod
    # def create(cls, token: str, user_id: int, expires_in_days: int = settings.REFRESH_TOKEN_EXPIRE_DAYS) -> "RefreshToken":
    #     expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
    #     return cls(token=token, user_id=user_id, expires_at=expires_at)