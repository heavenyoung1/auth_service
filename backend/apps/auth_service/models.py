from database import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
class User(SQLAlchemyBaseUserTableUUID, Base):
    pass