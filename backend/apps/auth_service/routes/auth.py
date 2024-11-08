from fastapi import APIRouter

from core.config import settings
from dependencies.fastapi_users_configuration import fastapi_users
from authentification.auth_backend import authentification_backend

auth_router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

auth_router.include_router(
    router=fastapi_users.get_auth_router(authentification_backend),
)
