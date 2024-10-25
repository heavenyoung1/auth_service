from apps.auth_service.models.base import Base
from ..mixins.id_int_pk import IdIntPkMixin
from typing import TYPE_CHECKING
from ..types.user_id import UserIdType

from fastapi_users.db import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)