from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class DetailOrderGuide(Base):
    __tablename__ = "detail_order_guides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sn_id = Column(String(255), ForeignKey("serial_numbers.sn_id"))
    order_guide_id = Column(Integer, ForeignKey("order_guides.id"))

    order_guide = relationship("OrderGuide", foreign_keys=[order_guide_id])
    sn = relationship("SerialNumber", foreign_keys=[sn_id])