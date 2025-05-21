from app.core.config import settings
from app.models.token import RefreshToken

from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from logging import Logger

# Объект для безопасного хеширования и проверки паролей с помощью библиотеки passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(original_password, hashed_password) -> bool:
    """
    Проверяет, соответствует ли введённый пароль его хешу.

    Args:
        original_password (str): Введённый пользователем пароль в открытом виде.
        hashed_password (str): Хешированный пароль из базы данных.

    Returns:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(original_password, hashed_password)

def get_password_hash(password) -> str:
    """
    Возвращает хеш от переданного пароля с использованием алгоритма bcrypt.

    Args:
        password (str): Пароль пользователя.

    Returns:
        str: Хешированное значение пароля.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """
    Создаёт JWT access-токен с ограниченным сроком действия.

    Args:
        data (dict): Словарь с данными (например, {'sub': 'user_id'}) для шифрования в токене.

    Returns:
        str: Сгенерированный access-токен (JWT).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def create_refresh_token(user_id: int, session: Session, logger: Logger) -> str:
    """
    Создаёт JWT refresh_token и сохраняет его в базе данных как объект RefreshToken.
    
    Args:
        user_id (int): ID пользователя. 
        session (Session): SQLAlchemy сессия для сохранения в базу.
    
    Returns:
        str: Сгенерированный refresh_token (JWT).
    """
    # Подготовка данных для JWT
    data = {"sub": str(user_id)}
    to_encode = data.copy() # Создаём копию словаря, чтобы не изменять оригинал
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": int(expire.timestamp())}) # Используем timestamp

    refresh_token_str = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user_id,
        expires_at=expire,
    )

    session.add(refresh_token)
    session.commit()

    return refresh_token_str