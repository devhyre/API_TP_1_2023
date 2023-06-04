from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class OrderGuide(Base):
    __tablename__ = "order_guides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    created_at = Column(DateTime, index=True)

    order = relationship("Order", foreign_keys=[order_id])