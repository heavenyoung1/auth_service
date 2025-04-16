from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite+pysqlite:///:memory:"
connect_args = {"echo: True"}

engine = create_engine(url, connect_args=connect_args)

Session = sessionmaker(engine)

def get_session():
    with Session(engine) as session:
        yield session
