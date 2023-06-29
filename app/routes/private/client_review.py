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
        #!OBTENER TODOS LAS ORDENES DEL CLIENTE QUE TENGAN EL ESTADO 3
        orders = db.query(OrderModel).filter(
            OrderModel.user_id == user[user_type]['numeroDocumento']).all()
        orders = [order for order in orders if order.state_id == 3]
        #!BUSCAR EN LOS DETALLES DE LAS ORDENES SI EL PRODUCTO QUE SE QUIERE CALIFICAR ESTA EN ALGUNA DE LAS ORDENES
        #!SI ESTA EN ALGUNA DE LAS ORDENES, SE PUEDE CALIFICAR
        #!SI NO ESTA EN NINGUNA DE LAS ORDENES, NO SE PUEDE CALIFICAR
        count = 0
        for order in orders:
            detail_orders = db.query(DetailOrderModel).filter(
                DetailOrderModel.order_id == order.id).all()
            detail_orders = [
                detail_order for detail_order in detail_orders if detail_order.product_id == review_data.product_id]
            if len(detail_orders) > 0:
                count += 1
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Debe haber realizado al menos una compra de este producto para poder realizar una reseña')
        else:
            #!CREAR LA RESEÑA
            client_review_db = ClientReviewModel(
                client_id=user[user_type]['id'],
                product_id=review_data.product_id,
                review=review_data.review,
                create_at=datetime.now(),
                punctuation=review_data.punctuation
            )
            db.add(client_review_db)
            db.commit()
            db.refresh(client_review_db)
            return client_review_db


@client_review.put('/actualizarReviewCliente/{id}', status_code=status.HTTP_202_ACCEPTED, name='CLIENTE - Actualizar la reseña de un Producto que le pertenece al Cliente')
async def actualizar_reseña_cliente(id: int, review_data: ClientReviewPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        #!Obtener la reseña
        client_review_db = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        if client_review_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro la reseña')
        #!Verificar que la reseña le pertenezca al cliente
        if client_review_db.client_id != user[user_type]['id']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No tiene permisos para realizar esta acción')
        client_review_db.review = review_data.review
        client_review_db.punctuation = review_data.punctuation
        db.commit()
        db.refresh(client_review_db)
        return client_review_db


@client_review.get('/admin/obtenerReviews', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener todas las reseñas hechas a los productos')
async def obtener_reseñas(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
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
                        if client.user_id == user.id:
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
async def obtener_reseñas_cliente (db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        client_reviews = db.query(ClientReviewModel).all()
        client_reviews = list(filter(lambda client_review: client_review.client_id == user[user_type]['id'], client_reviews))

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
        # Eliminar la reseña
        db.delete(client_review)
        db.commit()
        return {'message': 'Reseña eliminada satisfactoriamente'}
    else:
        client_review = db.query(ClientReviewModel).filter(
            ClientReviewModel.id == id).first()
        db.delete(client_review)
        db.commit()
        return {'message': 'Reseña eliminada satisfactoriamente'}
