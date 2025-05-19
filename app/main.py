from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.api.v1.auth import router as auth_router
from app.api.v1.test_routes import router as test_router
from app.database.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Код, выполняемый при остановке (если нужен)
    print("Application shutdown")

app = FastAPI(
            title="Сервис авторизации",
            version="0.1",
            lifespan=lifespan  # Укажи lifespan здесь
)

app.include_router(auth_router, prefix="/API/v0.1")
app.include_router(test_router, prefix="/API/v0.1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)