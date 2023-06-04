from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sn_id = Column(String(255), ForeignKey("sn.id"), index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), index=True)
    created_at = Column(DateTime)
    type_id = Column(Integer)

    sn = relationship("SerialNumber", foreign_keys=[sn_id])
    worker = relationship("Worker", foreign_keys=[worker_id])