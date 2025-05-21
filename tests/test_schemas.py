from sqlalchemy.orm.session import Session

from app.schemas.user import UserCreate


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
