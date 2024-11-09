from typing import TYPE_CHECKING

from models.base import Base
from mixins.id_int_pk import IdIntPkMixin
from app_types.user_id import UserIdType

from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
