from fastapi import FastAPI
import uvicorn
from auth_service.auth import router as auth_router


app = FastAPI(
        title="Booking Service",
        description="Creator HeavenYoung",
        version="0.0.1",
    )

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)