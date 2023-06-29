from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.client_review import ClientReview as ClientReviewModel
from app.models.product import Product as ProductModel
from app.models.user import User as UserModel
from app.models.client import Client as ClientModel

client_review_pu = APIRouter()

# OBTENER TODAS LAS RESEÑAS DE UN PRODUCTO


@client_review_pu.get('/obtenerReviewsProducto/{id}', status_code=status.HTTP_200_OK, name='Obtener reseñas de un producto por id')
async def obtener_reseñas_producto(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Producto no encontrado')
    else:
        client_reviews = db.query(ClientReviewModel).filter(
            ClientReviewModel.product_id == id).all()

        if len(client_reviews) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No hay reseñas para este producto')
        else:
            # Crear el Json de respuesta
            response = []
            # Recorrer las reseñas
            for client_review in client_reviews:
                # Obtener el cliente de la reseña
                client = db.query(ClientModel).filter(
                    ClientModel.id == client_review.client_id).first()
                # Obtener el usuario del cliente
                user = db.query(UserModel).filter(
                    UserModel.num_doc == client.user_id).first()
                # Crear el Json de la reseña
                review_json = {
                    'id': client_review.id,
                    'review': client_review.review,
                    'punctuation': client_review.punctuation,
                    'createdAt': client_review.created_at,
                    'client': {
                        'id': client.id,
                        'user': {
                            'numeroDocumento': user.num_doc,
                            'nombreCompleto': user.full_name,
                        },
                    },
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                    },
                }
                # Agregar el Json de la reseña al Json de respuesta
                response.append(review_json)
            # Retornar el Json de respuesta
            return response
