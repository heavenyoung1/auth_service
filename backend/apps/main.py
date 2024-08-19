from fastapi import FastAPI
import uvicorn
from auth_service.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)