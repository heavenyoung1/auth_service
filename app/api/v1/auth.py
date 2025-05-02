from app.core.config import settings
from app.database.db import get_session
from app.schemas.user import UserCreate, Token
from app.models.user import User
from app.core.security import get_password_to_hash, create_access_token, verify_password

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from logging import Logger, getLogger
from typing import Annotated

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=Token)
def register(
            user_in: UserCreate, 
            session: Session = Depends(get_session),
            logger: Logger = Depends(getLogger)
) -> Token:
    
    # Проверка существования пользователя
    db_user = session.query(User).filter(User.login == user_in.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Такой логин уже существует.")
    
    # Создание нового пользователя
    hashed_password = get_password_to_hash(user_in.password)
    db_user = User(
                    login=user_in.login,
                    fullname=user_in.fullname,
                    hashed_password=hashed_password,
                    role=user_in.role
                    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.info(f"Пользователь {user_in.login} успешно зарегистрирован с id {db_user.id}")

    # Генеарация токена
    access_token = create_access_token(data={"sub": user_in.login})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
    logger: Logger = Depends(getLogger)
) -> Token:
    
    logger.info(f"Попытка входа для login: {form_data.username}")

    # Проверка существования пользователя
    db_user = session.query(User).filter(User.login == form_data.username).first()

    # Проверка наличия логина в БД
    if not db_user:
        logger.warning(f"Неверный логин")
        raise HTTPException(status_code=401, detail="Неверный логин")
    
    # Проверка наличия логина в БД и сравнение его с хешированным паролем
    if db_user and not verify_password(form_data.password, db_user.hashed_password):
        logger.warning(f"Неверный пароль для {form_data.username}")
        raise HTTPException(status_code=401, detail="Неверный пароль")
    
    # Генеарация токена
    access_token = create_access_token(data={"sub": db_user.login})
    logger.info(f"Успешный вход для {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordRequestForm(tokenUrl="/API/v0.1/login")

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")
    user = session.query(User.filter(User.login == login).first())
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user