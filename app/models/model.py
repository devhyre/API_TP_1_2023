from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.db import Base
from sqlalchemy.orm import relationship

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))
    brand_id = Column(Integer, ForeignKey("brands.id"))

    brand = relationship("Brand", foreign_keys=[brand_id])