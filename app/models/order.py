from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    created_at = Column(DateTime, index=True)
    discount = Column(Integer)
    status_order = Column(Integer)

    user = relationship("User", foreign_keys=[user_id])