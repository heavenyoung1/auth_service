from fastapi import FastAPI
import uvicorn

from auth_service.demo_jwt_auth import router

app = FastAPI(
        title="Booking Service",
        description="Creator HeavenYoung",
        version="0.0.1",
    )

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)