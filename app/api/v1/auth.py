import secrets

from app.core.config import settings
from app.core.security import get_password_hash, create_access_token, create_refresh_token , verify_password
from app.database.db import get_session
from app.models.user import User
from app.models.token import RefreshToken
from app.schemas.user import UserCreate, UserReturn, Token
from app.schemas.token import RefreshTokenRequest

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from logging import Logger, getLogger
from typing import Annotated
from datetime import datetime, timedelta, timezone

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/API/v0.1/login")

@router.post("/register", response_model=Token,  summary="Регистрация нового пользователя", description="Регистрирует нового пользователя в системе.")
def register(
            user_in: UserCreate, 
            session: Session = Depends(get_session),
            logger: Logger = Depends(getLogger)
) -> Token:
    
    # Проверка существования пользователя
    db_user = session.query(User).filter(User.login == user_in.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Такой логин уже существует")
    
    # Создание нового пользователя
    hashed_password = get_password_hash(user_in.password)

    db_user = User(
                    login=user_in.login,
                    fullname=user_in.fullname,
                    hashed_password=hashed_password,
                    role=user_in.role
                    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    logger.info(f"Пользователь {user_in.login} успешно зарегистрирован, id {db_user.id}")

    # Генеарация access-token
    access_token = create_access_token(data={"sub": user_in.login})

    logger.info(f"Пользователь {user_in.login} успешно зарегистрирован, id: {db_user.id}")

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token, summary="Авторизация пользователя", description="Аутентифицирует пользователя и возвращает токен доступа.")
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
    
    # Генерация access-token
    access_token = create_access_token(data={"sub": db_user.login})

    # Генерация refresh-токен (сам токен JWT)
    refresh_token_str = create_refresh_token(
        user_id=db_user.id,
        session=session,
        logger=logger
    )

    logger.debug(f"Generated refresh_token: {refresh_token_str}")  # Проверяем, что токен создан
    if not refresh_token_str:
        logger.error("refresh_token_str пустой или None!!!!!!!!!!")
        raise HTTPException(status_code=500, detail="ошибка генерации refresh token!!!!!!!!!!")

    logger.info(f"Успешный вход для {form_data.username}")

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        }

    logger.debug(f"ОТВЕТ МОДЕЛИ: {response}!!!!!!")  # Проверяем, что возвращается

    return response

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session),
        logger: Logger = Depends(getLogger),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str = payload.get("sub")

        if login is None:
            logger.warning("Токен не содержит логина (поле 'sub')")
            raise HTTPException(status_code=401, detail="Токен не содержит логина (поле 'sub')")
        
    except JWTError as e:
        logger.warning(f"Ошибка проверки токена: {str(e)}")
        raise HTTPException(status_code=401, detail="Неверный или истекший токен")

    
    user = session.query(User).filter(User.login == login).first()

    if user is None:
        logger.warning(f"Пользователь c логином {login} не найден")
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    logger.info(f"Пользователь {login} успешно аутентифицирован")
    return user

@router.get(
        "/me", 
        response_model=UserReturn, 
        summary="Получение информации о текущем пользователе", 
        description="Возвращает информацию о пользователе, чей токен используется для аутентификации.")
def read_user_me(current_user = Depends(get_current_user)) -> User:
    return current_user


@router.post("/refresh", summary="", description="")
def refresh_token(
    token_data: RefreshTokenRequest,
    session: Session = Depends(get_session),
    logger: Logger = Depends(getLogger),
):
    logger.info("Попытка обновления токена")

    # Выборка refresh_token из БД
    refresh_token = session.query(RefreshToken).filter(RefreshToken.token == token_data.refresh_token).first()

    # Проверка существования refresh_token в БД
    if not refresh_token:
        logger.warning("Refresh-токен не найден")
        raise HTTPException(status_code=404, detail="Refresh-токен не найден")
    
    # Проверка срока действия токена
    if refresh_token.expires_at and refresh_token.expires_at < datetime.now(timezone.utc):
        logger.warning("Refresh-токен истёк")
        session.delete(refresh_token)
        session.commit()
        raise HTTPException(status_code=401, detail="Refresh-токен истек")
    
    # Выборка пользователя по refresh_token из БД
    user = session.query(User).filter(User.id == refresh_token.user_id).first()

    # Проверка существования пользователя по его refresh_token в БД
    if not user:
        logger.warning("Пользователь не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Генерация нового access-token
    access_token = create_access_token(data={"sub": user.login})

    logger.info(f"Access-токен успешно обновлён для пользователя {user.login}")

    return {
        "access_token": access_token,
        "refresh_token": token_data.refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout", summary="Выход пользователя из сессии", description="Выход пользователя из сессии")
def logout(
    token_data: RefreshTokenRequest, 
    session: Session = Depends(get_session),
    logger: Logger = Depends(getLogger),
):
    
    logger.info("Попытка выхода пользователя")

    # Выборка refresh_token из БД
    refresh_token = session.query(RefreshToken).filter(RefreshToken.token == token_data.refresh_token)

    # Проверка существования refresh_token в БД
    if not refresh_token:
        logger.warning("Refresh-токен не найден")
        raise HTTPException(status_code=404, detail="Refresh-токен не найден")
    
    session.delete(refresh_token)
    session.commit()

    logger.info("Пользователь вышел")

    return {"message": "Успешный выход"}
    
    