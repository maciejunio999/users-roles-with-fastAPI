from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

LocalSession = sessionmaker(autocommit=False, bind=engine, autoflush=False,)

Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()