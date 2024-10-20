from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

SECRET = "SECRET"

# Опеределяет что токен передаётся через заголовок HTTP-запроса Authorization: Bearer <token>
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy: #JWTStrategy - стратегия создания токена
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# Связывание транспорт и стратегию аутентификацию
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
