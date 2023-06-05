from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    code_payment = Column(String(255))
    created_at = Column(DateTime, index=True)
    total = Column(Float)

    order = relationship("Order", foreign_keys=[order_id])
    user = relationship("User", foreign_keys=[user_id])