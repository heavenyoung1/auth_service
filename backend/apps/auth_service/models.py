from fastapi_users.db import SQLAlchemyBaseUserTable
from base import Base
from mixins.id_int_pk import IdIntPkMixin

class User(SQLAlchemyBaseUserTable[int], Base, IdIntPkMixin):
    pass

