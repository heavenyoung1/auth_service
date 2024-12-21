from fastapi import APIRouter

from core.config import settings
from dependencies.fastapi_users_configuration import fastapi_users

from schemas.user import UserRead, UserUpdate


users_router = APIRouter(
    prefix=settings.api.users,
    tags=["Users"],
)

users_router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)

