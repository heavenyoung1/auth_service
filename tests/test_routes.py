from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_session

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/API/v0.1/test_db_session")
def test_db_session(session: Session = Depends(get_session)):
    result  = session.execute("SELECT 1").scalar()
    return {"ok": result == 1}
