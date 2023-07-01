from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sn_id  = Column(String(255), ForeignKey("serial_numbers.sn_id"), index=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    created_at = Column(DateTime)
    type_id = Column(Integer)

    sn = relationship("SerialNumber", foreign_keys=[sn_id])
    user = relationship("User", foreign_keys=[user_id])