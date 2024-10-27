from typing import TYPE_CHECKING, Annotated
from ..database import async_session_maker

from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_db(
        session: Annotated[
            "AsyncSession",
        ] = Depends(async_session_maker.get)):
    yield SQLAlchemyUserDatabase(session, User)