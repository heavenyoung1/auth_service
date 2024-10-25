from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseUserTable
from base import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    pass

