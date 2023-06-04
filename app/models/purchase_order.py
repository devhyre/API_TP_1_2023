from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)
    created_at = Column(DateTime, index=True)

    supplier = relationship("Supplier", foreign_keys=[supplier_id])