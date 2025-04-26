from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Объект для безопасного хеширования и проверки паролей с помощью библиотеки passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)