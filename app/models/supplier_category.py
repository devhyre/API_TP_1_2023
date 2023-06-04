from sqlalchemy import Column, Integer, ForeignKey,String
from sqlalchemy.orm import relationship
from app.core.db import Base

class SupplierCategory(Base):
    __tablename__ = "supplier_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, index=True)
    supplier_id = Column(String(12), ForeignKey("suppliers.num_doc"), index=True)

    supplier = relationship("Supplier", foreign_keys=[supplier_id])