from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, Token
from app.database.db import get_session
from app.models.user import User
from app.core.security import get_password_to_hash, create_access_token



router = APIRouter

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, session: Session = Depends(get_session)) -> User:
    db_user = session.query(User).filter(User.login == user_in.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Такой логин уже существует")
    hashed_password = get_password_to_hash(user_in.password)
    db_user = User(
                    login=user_in.login,
                    fullname=user_in.fullname,
                    hashed_password=hashed_password,
                    role=user_in.role
                    )
    session.add(db_user)
    session.commit()
    session.refresh()
    access_token = create_access_token(data={"sub": user_in.login})
    return {"access_token": access_token, "token_type": "bearer"}