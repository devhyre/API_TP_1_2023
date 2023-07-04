from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class RepairsMaintenance(Base):
    __tablename__ = "repairs_maintenance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_id = Column(Integer)
    type_id = Column(Integer)
    entry_date = Column(DateTime)
    departure_date = Column(DateTime, nullable=True)
    client_doc = Column(String(12))
    client_name = Column(String(150), nullable=True)
    client_email = Column(String(150), nullable=True)
    serial_number = Column(String(255))
    description = Column(String(255))
    note_diagnostic = Column(String(255), nullable=True)
    note_repair = Column(String(255), nullable=True)
    discount = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)

    worker = relationship("Worker", foreign_keys=[worker_id])