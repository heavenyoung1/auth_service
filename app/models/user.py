from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
Base = DeclarativeBase()

class User(Base):
    __tablename__ = "user"
    id = 

User.__tablename__
User.__mapper__