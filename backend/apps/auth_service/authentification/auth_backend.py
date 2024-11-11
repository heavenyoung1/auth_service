from fastapi_users.authentication import (
    AuthenticationBackend,
)

from authentification.strategy import get_database_strategy
from authentification.transport import bearer_transport

authentification_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
