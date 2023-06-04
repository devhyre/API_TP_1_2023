from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))
    path_image = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)
    discount = Column(Integer)
    warranty = Column(Integer)
    category_id = Column(Integer)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    status_id = Column(Integer)
    ranking = Column(Integer)

    brand = relationship("Brand", foreign_keys=[brand_id])
    model = relationship("Model", foreign_keys=[model_id])
    