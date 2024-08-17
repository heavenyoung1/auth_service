from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel

router = APIRouter()

class LoginSchema(BaseModel):
    username: str
    password: str

# Пример схемы для ответа
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenSchema)
async def login(user: LoginSchema):
    if user.username != "test" or user.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )