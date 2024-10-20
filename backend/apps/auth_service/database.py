from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from models import User
from base import Base
from fastapi_users import FastAPIUsers
import uuid
from user_manager import get_user_manager
from auth import auth_backend

from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/testpostgreserver"

# Настройка асинхронного движка
engine = create_async_engine(DATABASE_URL)
# Создание асинхронных сессий для работы с БД
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Создание таблиц в БД, если не существуют
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Получение объекта SQLAlchemyUserDatabase для управления пользователями
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)