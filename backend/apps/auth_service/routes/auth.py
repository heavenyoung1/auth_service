from fastapi import APIRouter

from core.config import settings
from dependencies.fastapi_users_configuration import fastapi_users
from authentification.auth_backend import authentification_backend
from schemas.user import UserCreate, UserRead


auth_router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

# /login
# /logout
auth_router.include_router(
    router=fastapi_users.get_auth_router(
        authentification_backend,
    ),
)

auth_router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
