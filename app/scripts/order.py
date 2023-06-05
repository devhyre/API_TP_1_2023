from app.schemas.order import OrderPost
from app.models.order import Order as OrderModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.detail_order import DetailOrder as DetailOrderModel


def create_order(db: Session, order: OrderPost):
    order_db = OrderModel(
        user_id = order.user_id,
        code_payment = order.code_payment,
        created_at = datetime.now(),
        total = order.total
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

def create_detail_order(db: Session, order_id: int, product_id: int, quantity: int):
    pass