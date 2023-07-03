from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Combo(Base):
    __tablename__ = "combos"

    id = Column(String(255), primary_key=True, index=True, unique=True)
    name = Column(String(100))
    description = Column(String(255))
    path_image = Column(String(100))
    case_id = Column(Integer, ForeignKey("products.id"))
    quantity_case = Column(Integer)
    motherboard_id = Column(Integer, ForeignKey("products.id"))
    quantity_motherboard = Column(Integer)
    procesador_id = Column(Integer, ForeignKey("products.id"))
    quantity_procesador = Column(Integer)
    ram_id = Column(Integer, ForeignKey("products.id"))
    quantity_ram = Column(Integer)
    almacenamiento_id = Column(Integer, ForeignKey("products.id"))
    quantity_almacenamiento = Column(Integer)
    cooler_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_cooler = Column(Integer, nullable=True)
    gpu_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_gpu = Column(Integer, nullable=True)
    fan_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_fan = Column(Integer, nullable=True)
    fuente_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_fuente = Column(Integer, nullable=True)
    created_at = Column(DateTime, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)

    case = relationship("Product", foreign_keys=[case_id])
    motherboard = relationship("Product", foreign_keys=[motherboard_id])
    procesador = relationship("Product", foreign_keys=[procesador_id])
    ram = relationship("Product", foreign_keys=[ram_id])
    almacenamiento = relationship("Product", foreign_keys=[almacenamiento_id])
    cooler = relationship("Product", foreign_keys=[cooler_id], nullable=True)
    gpu = relationship("Product", foreign_keys=[gpu_id], nullable=True)
    fan = relationship("Product", foreign_keys=[fan_id] , nullable=True)
    fuente = relationship("Product", foreign_keys=[fuente_id], nullable=True)
    worker = relationship("Worker", foreign_keys=[worker_id])
