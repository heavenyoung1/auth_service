import bcrypt
import jwt
from config import settings
from datetime import timedelta, datetime

def encode_jwt(
    payload: dict,
    private_key: settings.auth_jwt.private_key_path.read_text(),
    algorithm: settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    expire = ...
    to_encode.update(exp=expire)
    now = datetime.now()

    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded

def decode_jwt(
                token: str | bytes,
                public_key: settings.auth_jwt.public_key_path.read_text(),
                algorithm: settings.auth_jwt.algorithm,
               ):
    decoded = jwt.encode(
        token,
        public_key,
        algorithm=[algorithm],
    )
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
        password: str,
        hashed_password: bytes
        ) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )