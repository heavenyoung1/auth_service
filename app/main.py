from fastapi import FastAPI
import uvicorn

from app.api.v1.auth import router as auth_router
from app.api.v1.test_routes import router as test_router
from app.database.db import init_db

app = FastAPI(
            title="Сервис авторизации",
            version="0.1",
)

init_db() # Инициализация таблиц в БД, при старте приложения

app.include_router(auth_router, prefix="/API/v0.1")
app.include_router(test_router, prefix="/API/v0.1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)