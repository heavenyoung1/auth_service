from fastapi import Depends
from typing import Annotated
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from typing import TYPE_CHECKING
from dependencies.access_tokens import get_access_token_db
from core.config import settings

if TYPE_CHECKING:
    from ..models.access_token import AccessToken


def get_database_strategy(
    access_token_db: Annotated[
        AccessTokenDatabase["AccessToken"],
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
