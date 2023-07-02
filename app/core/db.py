from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from .config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
ScopedSession = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = ScopedSession.query_property()


def get_db():
    db = ScopedSession()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_session():
    return ScopedSession()


"""
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = SessionLocal()
        return cls._instance

def get_db():
    db = Database().session
    try:
        yield db
    finally:
        db.close()
        

def get_db_session():
    return Database().session
"""