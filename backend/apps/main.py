from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Booking Service",
    description="Creator HeavenYoung",
    version="0.0.1",
)

@app.get("/")
def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)