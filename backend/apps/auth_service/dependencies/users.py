from typing import TYPE_CHECKING, Annotated

from core.db_helper import db_helper
from models.user import User

from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield User.get_db(session=session)
