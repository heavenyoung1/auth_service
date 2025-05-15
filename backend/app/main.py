from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1.auth import router as auth_router
from app.api.v1.test_routes import router as test_router

app = FastAPI(
            title="Сервис авторизации",
            version="0.1",
)

app.include_router(auth_router, prefix="/API/v0.1")
app.include_router(test_router, prefix="/API/v0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)