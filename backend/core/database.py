from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/testpostgreserver"

engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

async_session_maker = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   expire_on_commit=False)

Base = declarative_base()