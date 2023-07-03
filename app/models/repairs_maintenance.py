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
    client_name = Column(String(150))
    client_email = Column(String(150))
    serial_number = Column(String(255))
    description = Column(String(255))
    note_diagnostic = Column(String(255))
    note_repair = Column(String(255))
    discount = Column(Integer)
    price = Column(Float)
    total = Column(Float)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)

    worker = relationship("Worker", foreign_keys=[worker_id])