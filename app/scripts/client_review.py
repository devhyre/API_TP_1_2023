from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
#!CLIENT REVIEW
from app.models.client_review import ClientReview as ClientReviewModel
from app.schemas.client_review import ClientReviewPost, ClientReviewPut
#!ORDER
from app.models.order import Order as OrderModel
#!ORDER DETAIL
from app.models.detail_order import DetailOrder as DetailOrderModel


def create_client_review(db: Session, user_id: str, client_id: int, client_review: ClientReviewPost):
    #!OBTENER TODOS LAS ORDENES DEL CLIENTE QUE TENGAN EL ESTADO 3
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id, OrderModel.status_order == 3).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Debe haber realizado al menos una compra para poder realizar una reseña de un producto')
    #!BUSCAR EN CADA ORDEN SI EXISTE EL PRODUCTO, SI EXISTE EN ALGUNA ORDEN, SE CREA LA RESEÑA
    for order in orders:
        detail_order = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == order.id, DetailOrderModel.product_id == client_review.product_id).first()
        if detail_order:
            #!CREAR RESEÑA
            client_review_db = ClientReviewModel(
                client_id = client_id,
                product_id = client_review.product_id,
                review = client_review.review,
                created_at = datetime.now(),
                punctuation = client_review.punctuation
            )
            db.add(client_review_db)
            db.commit()
            db.refresh(client_review_db)
            return client_review_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Debe haber realizado al menos una compra de este producto para poder realizar una reseña')
        
"""
Esta función busca las órdenes del cliente que tengan ciertos estados, verifica si el cliente ha comprado el producto para el cual desea dejar una reseña y, en ese caso, crea la reseña y la guarda en la base de datos. Si el cliente no ha realizado ninguna compra o no ha comprado el producto en cuestión, se lanza una excepción.
"""

def update_client_review(db: Session, client_id: int, client_review_id: int, client_review: ClientReviewPost):
    client_review_db = db.query(ClientReviewModel).filter(ClientReviewModel.id == client_review_id).first()
    if not client_review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontró la reseña')
    if client_review_db.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_review_db.review = client_review.review
        client_review_db.punctuation = client_review.punctuation
        db.commit()
        db.refresh(client_review_db)
        return client_review_db
    
"""
Esta función busca la reseña en la base de datos, verifica que el cliente que desea actualizar la reseña sea el mismo que la creó y, en ese caso, actualiza la reseña y la guarda en la base de datos. Si el cliente no es el mismo que creó la reseña, se lanza una excepción.
"""