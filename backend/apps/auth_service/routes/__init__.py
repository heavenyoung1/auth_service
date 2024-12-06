__all__ = (
    "auth_router",
    "router",
    "users_router"
)

from routes.auth import auth_router
from routes.router import router
from routes.users import router as users_router
