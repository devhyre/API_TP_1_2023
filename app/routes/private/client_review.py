from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.scripts.client_review import create_client_review, update_client_review
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.client_review import ClientReview as ClientReviewModel
from app.schemas.client_review import ClientReview, ClientReviewPost, ClientReviewPut
from typing import List

client_review = APIRouter()

@client_review.post('/crearReseñaCliente')
async def crear_reseña_cliente(review_data: ClientReviewPost,db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_review = create_client_review(db, user[user_type]['numeroDocumento'], user[user_type]['id'], review_data)
        return client_review
    
@client_review.put('/actualizarReseñaCliente/{id}', response_model=ClientReview)
async def actualizar_reseña_cliente(id:int, review_data: ClientReviewPut,db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_review = update_client_review(db, user[user_type]['id'],id, review_data)
        return client_review
    
@client_review.get('/obtenerReseñasCliente', response_model=List[ClientReview])
async def obtener_reseñas_cliente(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_reviews = db.query(ClientReviewModel).filter(ClientReviewModel.client_id == user[user_type]['id']).all()
        return client_reviews
    
@client_review.get('/obtenerReseñas', response_model=ClientReview)
async def obtener_reseñas(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_reviews = db.query(ClientReviewModel).all()
        return client_reviews

@client_review.get('/obtenerReseña/{id}', response_model=ClientReview)
async def obtener_reseña(id:int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_review = db.query(ClientReviewModel).filter(ClientReviewModel.id == id).first()
        return client_review
    
@client_review.delete('/eliminarReseña/{id}')
async def eliminar_reseña(id:int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        client_review = db.query(ClientReviewModel).filter(ClientReviewModel.id == id).first()
        db.delete(client_review)
        db.commit()
        return {'message': 'Reseña eliminada satisfactoriamente'}