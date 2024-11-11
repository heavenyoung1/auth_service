from fastapi_users import FastAPIUsers

from models.user import User
from dependencies.user_manager import get_user_manager
from authentification.auth_backend import authentification_backend as auth_backend
from app_types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)
