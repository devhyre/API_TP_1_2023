from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class DetailCombo(Base):
    __tablename__ = "detail_combos"

    id = Column(String(100), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    combo_id = Column(String(255), ForeignKey("combos.id"))

    product = relationship("Product", foreign_keys=[product_id])
    combo = relationship("Combo", foreign_keys=[combo_id])
    