from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class ClientReview(Base):
    __tablename__ = "client_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    review = Column(String(255))
    created_at = Column(DateTime, index=True)
    punctuation = Column(Integer)

    client = relationship("Client", foreign_keys=[client_id])
    product = relationship("Product", foreign_keys=[product_id])