from fastapi import APIRouter
from routes.auth import auth_router
from routes.users import router as users_router

# Основной маршрутизатор приложения
router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
