from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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

    except Exception as e:
        print(e)
        db.rollback()
        raise
    finally:
        db.close()
        

def get_db_session():
    return Database().session