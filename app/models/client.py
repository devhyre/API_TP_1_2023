from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    created_at = Column(DateTime)
    last_connection = Column(DateTime)

    user = relationship("User", foreign_keys=[user_id])