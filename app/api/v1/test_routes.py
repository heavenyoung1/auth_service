from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.db import get_session

router = APIRouter(tags=["test"])

@router.get("/", summary="Домашний эндпоинт", description="Домашний эндпоинт")
def read_root():
    return {"Hello": "World"}

@router.get("/test", summary="Тестовый эндпоинт", description="Тестовый эндпоинт")
async def test():
    return {"message": "Hello from FastAPI"}

@router.get("/test_db_session", summary="Тестовое подключение к БД", description="Тестовое подключение к БД")
def test_db_session(session: Session = Depends(get_session)):
    result  = session.execute(text("SELECT 1")).scalar()
    return {"ok": result == 1}


