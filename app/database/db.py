from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Annotated

from app.core.config import settings
from app.models.user import Base

connect_args = {"echo": True}

engine = create_engine(settings.DATABASE_URL, echo=True) #connect_args=connect_args

Session = sessionmaker(engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
