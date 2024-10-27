from fastapi import APIRouter
from ..core.config import settings

auth_router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)
