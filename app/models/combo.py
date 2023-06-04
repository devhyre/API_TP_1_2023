from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Combo(Base):
    __tablename__ = "combos"

    id = Column(String(255), primary_key=True, index=True, unique=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)

    product = relationship("Product", foreign_keys=[product_id])
    worker = relationship("Worker", foreign_keys=[worker_id])
