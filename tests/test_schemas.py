from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from app.models.token import RefreshToken
from app.schemas.user import UserCreate
from tests.conftest import test_session
from app.core.logger import logger
from datetime import datetime, timezone, timedelta


def test_user_create_valid(test_session: Session):
    user = UserCreate(
        login="test@example.com", 
        fullname="Test User", 
        password="123456", 
        role="user")
    assert user.login == "test@example.com"
    assert user.fullname == "Test User"
    assert user.password == "123456"
    assert user.role == "user"

# Можно написать еще схемы, но нужно ли?)
