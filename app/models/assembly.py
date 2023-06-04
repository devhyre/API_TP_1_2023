from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Assembly(Base):
    __tablename__ = "assemblies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    major_product_id = Column(Integer, ForeignKey("products.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    description = Column(String(255))

    major_product = relationship("Product", foreign_keys=[major_product_id])
    product = relationship("Product", foreign_keys=[product_id])

"""
TABLA DE LOS MEJORES PRODUCTOS PARA CADA PRODUCTO MAS UNA DESCRIPCION DE PORQUE ES EL MEJOR
EJEMPLO:
    PRODUCTO 1:
        PRODUCTO 2: PORQUE ES MAS BARATO
        PRODUCTO 3: PORQUE TIENE MAS RANKING - RECOMENDADO
        PRODUCTO 4: PORQUE TIENE MAS DESCUENTO
        PRODUCTO 5: PORQUE TIENE MAS GARANTIA
"""