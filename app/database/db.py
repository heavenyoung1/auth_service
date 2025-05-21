from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Annotated, Generator

from app.core.config import settings
from app.models.user import Base

# Создание движка SQLAlchemy
engine = create_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

def init_db():
    """Создаёт все таблицы в базе данных на основе моделей."""
    try:
        print(f"Попытка создания таблиц с движком: {engine}")
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы успешно созданы.")
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
        raise

def get_session() -> Generator[Session, None, None]:
    """Предоставляет сессию БД как зависимость FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Используемый тип для зависимостей FastAPI
SessionDep = Annotated[Session, Depends(get_session)]
