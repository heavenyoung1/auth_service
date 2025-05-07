from app.api.v1.auth import router as auth_router
from app.api.v1.test_routes import router as test_router

from fastapi import FastAPI
import uvicorn

app = FastAPI(
            title="Тестовый сервис авторизации",
            description="Креатор, Фаундер и прочие челы с горы",
            version="0.1",
)
app.include_router(auth_router, prefix="/API/v0.1")
app.include_router(test_router, prefix="/API/v0.1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)