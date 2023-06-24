from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.client_review import ClientReview as ClientReviewModel
from app.models.product import Product as ProductModel
from app.models.user import User as UserModel
from app.models.client import Client as ClientModel

client_review_pu = APIRouter()

#OBTENER TODAS LAS RESEÑAS DE UN PRODUCTO
@client_review_pu.get('/obtenerReviewsProducto/{id}', status_code=status.HTTP_200_OK)
async def obtener_reseñas_producto(id:int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto no encontrado')
    else:
        client_reviews = db.query(ClientReviewModel).filter(ClientReviewModel.product_id == id).all()
        Data = {
            "id": [],
            "client_id": [],
            "product_id": [],
            "review": [],
            "created_at": [],
            "punctuation": [],
            "client_name": [],
        }
        #Obtener los datos del cliente y usar el user_id para obtener el nombre del cliente
        client = db.query(ClientModel).filter(ClientModel.id == ClientReviewModel.client_id).first()
        user = db.query(UserModel).filter(UserModel.id == client.user_id).first()
        for client_review in client_reviews:
            Data["id"].append(client_review.id)
            Data["client_id"].append(client_review.client_id)
            Data["product_id"].append(client_review.product_id)
            Data["review"].append(client_review.review)
            Data["created_at"].append(client_review.created_at)
            Data["punctuation"].append(client_review.punctuation)
            Data["client_name"].append(user.full_name)
        return Data