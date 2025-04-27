from app.api.v1.auth import router as auth_router

from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(auth_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)