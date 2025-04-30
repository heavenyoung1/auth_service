from sqlalchemy.orm import Session
from app.database.db import engine, get_session
from app.models.user import User, Role

def test_connection():
    with next(get_session()) as session:
        user = User(login="testId", fullname="Test User", hashed_password="password", role=Role.USER)
        session.add(user)
        session.commit()
        db_user = session.query(User).filter(User.login == "testId").first()
        print(db_user)

if __name__ == "__main__":
    test_connection()
