from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.token import RefreshToken

# Для тестов
# from jose.jwt import decode
#--------

# Объект для безопасного хеширования и проверки паролей с помощью библиотеки passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Проверка пароля - сравнение простого и хешированного паролей
def verify_password(original_password, hashed_password):
    return pwd_context.verify(original_password, hashed_password)

# Хеширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Создание ACCESS-токена для регистрации пользователей
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def create_refresh_token(user_id: int, session: Session) -> str:
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
    to_encode.update({"exp": expire})

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




# token = create_refresh_token({"sub": "test"})
# header = decode(token, key="12343434" ,options={"verify_signature": False}, algorithms=["HS256"])
# print(header)