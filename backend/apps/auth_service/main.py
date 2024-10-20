import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth import auth_backend
from user_manager import get_user_manager

from database import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

