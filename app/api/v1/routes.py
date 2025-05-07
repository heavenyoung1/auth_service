from fastapi import APIRouter

router = APIRouter(tags=["base"])

@router.get("/test")
async def test():
    return {"message": "Hello from FastAPI"}