from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.client_review import ClientReview as ClientReviewModel
from app.schemas.client_review import ClientReviewPost, ClientReviewPut
from app.models.order import Order as OrderModel
from app.models.user import User as UserModel
from app.models.product import Product as ProductModel
from app.models.order import Order as OrderModel
from app.models.detail_order import DetailOrder as DetailOrderModel
from datetime import datetime
from app.models.client import Client as ClientModel

client_review = APIRouter()


@client_review.post('/crearReviewCliente', status_code=status.HTTP_201_CREATED, name='CLIENTE - Crear reseña de un Producto')
async def crear_reseña_cliente(review_data: ClientReviewPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # OBTENER TODOS LAS ORDENES DEL CLIENTE QUE TENGAN EL ESTADO 3
        orders = db.query(OrderModel).filter(
            OrderModel.user_id == user[user_type]['numeroDocumento'], OrderModel.status_order == 3).all()

        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Debe haber realizado al menos una compra para poder realizar una reseña')

        # Verifica si el producto está en alguna de las órdenes
        count = db.query(DetailOrderModel).filter(DetailOrderModel.order_id.in_(
            [order.id for order in orders]), DetailOrderModel.product_id == review_data.product_id).count()

        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Debe haber realizado al menos una compra de este producto para poder realizar una reseña')

        # Crear la reseña
        client_review_db = ClientReviewModel(
            client_id=user[user_type]['id'],
            product_id=review_data.product_id,
            review=review_data.review,
            created_at=datetime.now(),
            punctuation=review_data.punctuation
        )
        db.add(client_review_db)

        # OBTENER TODAS LAS RESEÑAS DEL PRODUCTO
        client_reviews = db.query(ClientReviewModel).filter(
            ClientReviewModel.product_id == review_data.product_id).all()
        # OBTENER EL PROMEDIO DE LAS RESEÑAS
        if len(client_reviews) > 0:
            average = sum(
                review.punctuation for review in client_reviews) / len(client_reviews)
        else:
            average = 0
        # ACTUALIZAR EL RANKING DEL PRODUCTO
        db.query(ProductModel).filter(ProductModel.id ==
                                      review_data.product_id).update({ProductModel.ranking: average})
        client_review_created = db.query(ClientReviewModel).filter(
            ClientReviewModel.client_id == user[user_type]['id']).order_by(ClientReviewModel.id.desc()).first()
        return {'message': 'Reseña creada correctamente', 'data': client_review_created}


@client_review.put('/actualizarReviewCliente/{id}', status_code=status.HTTP_202_ACCEPTED, name='CLIENTE - Actualizar la reseña de un Producto que le pertenece al Cliente')
async def actualizar_reseña_cliente(id: int, review_data: ClientReviewPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener la reseña
        client_review_db = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        if client_review_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro la reseña')
        # Verificar que la reseña le pertenezca al cliente
        if client_review_db.client_id != user[user_type]['id']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No tiene permisos para realizar esta acción')
        # Actualizar la reseña y la puntuación
        db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).update({ClientReviewModel.review: review_data.review, ClientReviewModel.punctuation: review_data.punctuation})
        # Obtener todas las reseñas del producto
        client_reviews = db.query(ClientReviewModel).filter(
            ClientReviewModel.product_id == client_review_db.product_id).all()
        # Obtener el promedio de las reseñas
        if len(client_reviews) > 0:
            average = sum(
                review.punctuation for review in client_reviews) / len(client_reviews)
        else:
            average = 0
        # Actualizar el ranking del producto
        db.query(ProductModel).filter(ProductModel.id ==
                                      client_review_db.product_id).update({ProductModel.ranking: average})
        client_review_updated = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        return {'message': 'Reseña actualizada correctamente', 'data': client_review_updated}


@client_review.get('/admin/obtenerReviews', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener todas las reseñas hechas a los productos')
async def obtener_reseñas (db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []
        # Obtener todas las reseñas
        client_reviews = db.query(ClientReviewModel).all()
        # Obtener los productos
        products = db.query(ProductModel).all()
        # Obtener los clientes
        clients = db.query(ClientModel).all()
        # Obtener los usuarios
        users = db.query(UserModel).all()
        # Recorrer las reseñas
        for client_review in client_reviews:
            # Crear el Json de la reseña
            review_json = {
                'id': client_review.id,
                'review': client_review.review,
                'punctuation': client_review.punctuation,
                'created_at': client_review.created_at,
                'product': {},
                'client': {}
            }
            # Recorrer los productos
            for product in products:
                # Verificar si el producto de la reseña es igual al producto actual
                if client_review.product_id == product.id:
                    # Crear el Json del producto
                    product_json = {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price
                    }
                    # Agregar el producto a la reseña
                    review_json['product'] = product_json
            # Recorrer los clientes
            for client in clients:
                # Verificar si el cliente de la reseña es igual al cliente actual
                if client_review.client_id == client.id:
                    # Crear el Json del cliente
                    client_json = {
                        'id': client.id,
                        'user': {}
                    }
                    # Recorrer los usuarios
                    for user in users:
                        # Verificar si el usuario del cliente es igual al usuario actual
                        if client.user_id == user.num_doc:
                            # Crear el Json del usuario
                            user_json = {
                                'num_doc': user.num_doc,
                                'full_name': user.full_name,
                            }
                            # Agregar el usuario al cliente
                            client_json['user'] = user_json
                    # Agregar el cliente a la reseña
                    review_json['client'] = client_json
            # Agregar la reseña al Json de respuesta
            response.append(review_json)
        return response


@client_review.get('/obtenerReviewsCliente', status_code=status.HTTP_200_OK, name='CLIENTE - Obtener todas las reseñas hechas a los productos por el cliente que esta logueado')
async def obtener_reseñas_cliente(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        client_reviews = db.query(ClientReviewModel).all()
        client_reviews = list(filter(
            lambda client_review: client_review.client_id == user[user_type]['id'], client_reviews))

        if len(client_reviews) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No se encontraron reseñas')

        # Crear el Json de respuesta
        response = []
        # Obtener los productos
        products = db.query(ProductModel).all()
        # Recorrer las reseñas
        for client_review in client_reviews:
            # Crear el Json de la reseña
            review_json = {
                'id': client_review.id,
                'review': client_review.review,
                'punctuation': client_review.punctuation,
                'created_at': client_review.created_at,
                'product': {}
            }
            # Recorrer los productos
            for product in products:
                # Verificar si el producto de la reseña es igual al producto actual
                if client_review.product_id == product.id:
                    # Crear el Json del producto
                    product_json = {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price
                    }
                    # Agregar el producto a la reseña
                    review_json['product'] = product_json
            # Agregar la reseña al Json de respuesta
            response.append(review_json)
        return response


@client_review.get('/obtenerReview/{id}', status_code=status.HTTP_200_OK, name='CLIENTE - Obtener una reseña hecha a un producto por el cliente que esta logueado')
async def obtener_reseña(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        client_review = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        if client_review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No se encontró la reseña')
        if client_review.client_id != user[user_type]['id']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No tiene permisos para realizar esta acción')
        # Crear el Json de respuesta
        response = {
            'id': client_review.id,
            'review': client_review.review,
            'punctuation': client_review.punctuation,
            'created_at': client_review.created_at,
            'product': {}
        }
        # Obtener los productos
        products = db.query(ProductModel).all()
        # Recorrer los productos
        for product in products:
            # Verificar si el producto de la reseña es igual al producto actual
            if client_review.product_id == product.id:
                # Crear el Json del producto
                product_json = {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price
                }
                # Agregar el producto a la reseña
                response['product'] = product_json
        return response


@client_review.delete('/eliminarReview/{id}', status_code=status.HTTP_200_OK, name='CLIENTE|ADMINISTRADOR|TRABAJADOR - Eliminar una reseña hecha a un producto')
async def eliminar_reseña(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        # Obtener la reseña
        client_review = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        if client_review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No se encontró la reseña')
        if client_review.client_id != user[user_type]['id']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No tiene permisos para realizar esta acción')

        # Almacenar el producto
        product_id_temp = client_review.product_id
        # Eliminar la reseña
        db.delete(client_review)
        # Obtener todas las reseñas del producto
        client_reviews = db.query(ClientReviewModel).filter(
            ClientReviewModel.product_id == product_id_temp).all()
        # Obtener el promedio de las reseñas
        if len(client_reviews) > 0:
            average = sum(
                review.punctuation for review in client_reviews) / len(client_reviews)
        else:
            average = 0
        # Actualizar el promedio del producto
        db.query(ProductModel).filter(ProductModel.id ==
                                      product_id_temp).update({ProductModel.ranking: average})
        return {'message': 'Reseña eliminada correctamente'}
