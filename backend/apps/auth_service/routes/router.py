from fastapi import APIRouter
from routes.auth import auth_router

# Основной маршрутизатор приложения
router = APIRouter()

router.include_router(auth_router)
