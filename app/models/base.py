from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Базовый класс для всех моделей приложения """
    pass

# Импортируем модели, чтобы они добавлялись в Base.metadata
# from app.models.user import User
# from app.models.token import RefreshToken