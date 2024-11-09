from fastapi_users import FastAPIUsers

from models.user import User
from user_manager import get_user_manager
from authentification import auth_backend
from app_types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)
