from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_session
from sqlalchemy import text

router = APIRouter(tags=["test"])

@router.get("/test_db_session")
def test_db_session(session: Session = Depends(get_session)):
    result  = session.execute(text("SELECT 1")).scalar()
    return {"ok": result == 1}

