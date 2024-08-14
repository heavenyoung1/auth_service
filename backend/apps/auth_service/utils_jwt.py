import jwt
import starlette
from config import settings

def encode_jwt(
                payload: str,
                private_key: str,
                algorithm: str
                ):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm,
    )
    return encoded

def decode_jwt(
                token: str,
                public_key: str,
                algorithm: str
               ):
    decoded = jwt.encode(
        token,
        public_key,
        algorithm,
    )
    return decoded
