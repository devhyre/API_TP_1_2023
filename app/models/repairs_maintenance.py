from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class RepairsMaintenance(Base):
    __tablename__ = "repairs_maintenance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_service_id = Column(Integer)
    serial_number_id = Column(String(255), index=True)
    created_at = Column(DateTime)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)
    description = Column(String(255))
    note = Column(String(255))
    status_id = Column(Integer)
    discount = Column(Integer)
    total = Column(Float)

    worker = relationship("Worker", foreign_keys=[worker_id])