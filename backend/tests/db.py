from sqlalchemy.ext.declarative import DeclarativeMeta#, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/testpostgreserver'

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

async def get_async_session():
    async with async_session_maker() as session:
        yield session

async def get_user_db(session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы!")

async def check_db_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]
        print(f"Connected to database: {db_name}")

async def check_tables():
    async with engine.connect() as connection:
        result = await connection.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        ))
        tables = result.fetchall()
        # Предположим, что строки возвращаются в виде кортежей
        print(f"Existing tables: {[row[0] for row in tables]}")

async def create_schema():
    async with engine.connect() as connection:
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS your_schema;"))

async def main():
    # Проверим подключение к базе данных
    await check_db_connection()

    #await create_schema()

    # Создадим таблицы
    #await create_db_and_tables()

    # Проверим существующие таблицы
    #await check_tables()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())