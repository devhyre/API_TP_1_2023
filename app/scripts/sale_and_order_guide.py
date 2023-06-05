from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.sale import SalePost, SalePut
from app.models.sale import Sale as SaleModel
from app.schemas.order_guide import OrderGuidePost, OrderGuidePut
from app.models.order_guide import OrderGuide as OrderGuideModel

def create_sale(db: Session, sale: SalePost, order_id: int, user_id: str):
    sale_db = SaleModel(
        order_id = order_id,
        user_id = user_id,
        code_payment = sale.code_payment,
        created_at = datetime.now(),
        total = sale.total
    )
    db.add(sale_db)
    db.commit()
    db.refresh(sale_db)
    return sale_db

def get_sale_by_id(db: Session, id: int):
    return db.query(SaleModel).filter(SaleModel.id == id).first()

def get_sales(db: Session):
    return db.query(SaleModel).all()

def update_sale(db: Session, sale: SalePut, id: int):
    sale_db = db.query(SaleModel).filter(SaleModel.id == id).first()
    sale_db.code_payment = sale.code_payment
    sale_db.total = sale.total
    db.commit()
    db.refresh(sale_db)
    return sale_db

def create_order_guide(db: Session, order_id: int):
    order_guide_db = OrderGuideModel(
        order_id = order_id,
        created_at = datetime.now(),
    )
    db.add(order_guide_db)
    db.commit()
    db.refresh(order_guide_db)
    return order_guide_db

def get_order_guide_by_id(db: Session, id: int):
    return db.query(OrderGuideModel).filter(OrderGuideModel.id == id).first()

def get_order_guides(db: Session):
    return db.query(OrderGuideModel).all()

def create_detail_order_guide(db: Session, order_guide_id: int):
    pass