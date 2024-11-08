from fastapi import APIRouter

from core.config import settings

from auth import auth_router

router = APIRouter()

router.include_router(auth_router)
