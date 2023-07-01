from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class HistoryRM(Base):
    __tablename__ = "history_rm"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status_id = Column(Integer)
    date = Column(DateTime)
    description = Column(String(255))
    note_diagnostic = Column(String(255))
    note_repair = Column(String(255))
    repairs_maintenance_id = Column(Integer, ForeignKey("repairs_maintenance.id"), index=True)

    repairs_maintenance = relationship("RepairsMaintenance", foreign_keys=[repairs_maintenance_id])