from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    num_doc = Column(String(12), primary_key=True, index=True, unique=True)
    type_doc = Column(Integer, index=True)
    username = Column(String(20), index=True, unique=True)
    full_name = Column(String(100), index=True)
    email = Column(String(100), index=True, unique=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)