import jwt
import starlette
from config import settings

def encode_jwt(payload, private_key, algorithm):
    encoded = jwt.encode(
        payload,
        private_key=settings.auth_jwt.private_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm,
    )
    return encoded


def decode_jwt(token, public_key, algorithm):
    decoded = jwt.encode(
        token,
        public_key=settings.auth_jwt.public_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm,
    )
    return decoded
