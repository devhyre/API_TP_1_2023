from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Combo(Base):
    __tablename__ = "combos"

    id = Column(String(255), primary_key=True, index=True, unique=True)
    name = Column(String(100))
    description = Column(String(255))
    path_image = Column(String(100))
    case_id = Column(Integer)
    quantity_case = Column(Integer)
    motherboard_id = Column(Integer)
    quantity_motherboard = Column(Integer)
    procesador_id = Column(Integer)
    quantity_procesador = Column(Integer)
    ram_id = Column(Integer)
    quantity_ram = Column(Integer)
    almacenamiento_id = Column(Integer)
    quantity_almacenamiento = Column(Integer)
    cooler_id = Column(Integer, nullable=True)
    quantity_cooler = Column(Integer, nullable=True)
    gpu_id = Column(Integer, nullable=True)
    quantity_gpu = Column(Integer, nullable=True)
    fan_id = Column(Integer, nullable=True)
    quantity_fan = Column(Integer, nullable=True)
    fuente_id = Column(Integer, nullable=True)
    quantity_fuente = Column(Integer, nullable=True)
    created_at = Column(DateTime, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)

    worker = relationship("Worker", foreign_keys=[worker_id])
