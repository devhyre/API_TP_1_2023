from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class DetailPurchaseOrder(Base):
    __tablename__ = "detail_purchase_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))

    product = relationship("Product", foreign_keys=[product_id])
    purchase_order = relationship("PurchaseOrder", foreign_keys=[purchase_order_id])