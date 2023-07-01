from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class SerialNumber(Base):
    __tablename__ = "serial_numbers"

    sn_id = Column(String(255), primary_key=True, index=True, unique=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    supplier_id = Column(String(12), ForeignKey("suppliers.num_doc"), index=True, nullable=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    status_id = Column(Integer, index=True)
    entrance_at = Column(DateTime, index=True)
    departure_at = Column(DateTime, index=True)

    product = relationship("Product", foreign_keys=[product_id])
    supplier = relationship("Supplier", foreign_keys=[supplier_id])
    user = relationship("User", foreign_keys=[user_id])