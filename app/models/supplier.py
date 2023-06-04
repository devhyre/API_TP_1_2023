from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    num_doc = Column(String(12), primary_key=True, index=True, unique=True)
    name = Column(String(150), index=True)
    num_doc_representative = Column(String(12), index=True)
    name_representative = Column(String(150), index=True)
    email = Column(String(100), index=True)
    phone = Column(String(20), index=True)
    status = Column(Boolean, default=True)