from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

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

# Создание REFRESH-токена для логина пользователей
def create_refresh_token(data: dict):
    to_encode = data.copy() # Создаём копию словаря, чтобы не изменять оригинал
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_frsh_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_frsh_token


# token = create_refresh_token({"sub": "test"})
# header = decode(token, key="12343434" ,options={"verify_signature": False}, algorithms=["HS256"])
# print(header)