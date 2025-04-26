from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Объект для безопасного хеширования и проверки паролей с помощью библиотеки passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Проверка пароля - сравнение простого и хешированного паролей
def verify_password(original_password, hashed_password):
    return pwd_context.verify(original_password, hashed_password)

# Хеширование пароля
def get_password_to_hash(password):
    return pwd_context.hash(password)

# Создание JWT-токена для аутентификации пользователей
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt