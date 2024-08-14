from fastapi import APIRouter, Depends

from schemas import UserSchema
import utils_jwt as auth_util
from pydantic import BaseModel

class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username="john",
    password=auth_util.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=auth_util.hash_password("qwertyuiop"),
    email="sam@example.com",
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}

def validate_auth_user():
    pass

@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user())):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_util.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
