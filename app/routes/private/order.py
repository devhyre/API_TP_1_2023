from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.order import Order as OrderModel
from app.schemas.order import OrderPost
from app.models.detail_order import DetailOrder as DetailOrderModel
from app.schemas.detail_order import DetailOrderPost
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.product import Product as ProductModel
from app.models.user import User as UserModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel

order = APIRouter()

# Obtener orden por id
@order.get('/obtenerOrden/{id}', status_code=status.HTTP_200_OK, name='Obtener orden por id')
async def obtener_orden(id: int, db: Session = Depends(get_db)):
    order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
    if not order_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la orden')
    return order_db

# Obtener contadores de ordenes
@order.get('/obtenerContadoresOrdenes', status_code=status.HTTP_200_OK, name='Obtener contadores de ordenes')
async def obtener_contadores_ordenes(db: Session = Depends(get_db)):
    # Obtener todas las ordenes
    orders_db = db.query(OrderModel).all()
    # Contadores
    count_orders = len(orders_db)
    count_orders_pending = len(
        [order for order in orders_db if order.status_order == 1])
    count_orders_in_approved = len(
        [order for order in orders_db if order.status_order == 2])
    count_orders_in_delivered = len(
        [order for order in orders_db if order.status_order == 3])
    count_orders_in_refused = len(
        [order for order in orders_db if order.status_order == 4])
    count_orders_in_canceled = len(
        [order for order in orders_db if order.status_order == 5])
    count_orders_in_return = len(
        [order for order in orders_db if order.status_order == 6])
    count_orders_in_refund = len(
        [order for order in orders_db if order.status_order == 7])
    count_orders_in_paid = len(
        [order for order in orders_db if order.status_order == 8])
    count_orders_in_ready = len(
        [order for order in orders_db if order.status_order == 9])
    
    response = {
        'count_orders': count_orders,
        'count_orders_pending': count_orders_pending,
        'count_orders_in_approved': count_orders_in_approved,
        'count_orders_in_delivered': count_orders_in_delivered,
        'count_orders_in_refused': count_orders_in_refused,
        'count_orders_in_canceled': count_orders_in_canceled,
        'count_orders_in_return': count_orders_in_return,
        'count_orders_in_refund': count_orders_in_refund,
        'count_orders_in_paid': count_orders_in_paid,
        'count_orders_in_ready': count_orders_in_ready,
    }
    return response

@order.get('/listadoEstadosOrden', status_code=status.HTTP_200_OK, name='Listado de estados de orden')
async def listar_estados_orden(db: Session = Depends(get_db)):
    states = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 4).all()
    return [{'id': state.id_table, 'description': state.description} for state in states]


@order.get('/admin/obtenerOrdenes', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener ordenes')
async def obtener_ordenes(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener todas las ordenes
        orders_db = db.query(OrderModel).all()
        # Obtener todos los detalles de orden
        details_db = db.query(DetailOrderModel).all()
        # Obtener todos los productos
        products_db = db.query(ProductModel).all()
        # Obtener todas las categorias
        categories_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 3).all()
        categories_db = [
            {'id': category.id_table, 'description': category.description} for category in categories_db]
        # Obtener todos los modelos
        models_db = db.query(ModelModel).all()
        # Obtener todas las marcas
        brands_db = db.query(BrandModel).all()
        # Obtener todos los estados de producto
        states_product_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        states_product_db = [
            {'id': state.id_table, 'description': state.description} for state in states_product_db]
        # Obtener todos los estados de orden
        states_order_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 4).all()
        states_order_db = [
            {'id': state.id_table, 'description': state.description} for state in states_order_db]

        # Crear el Json de respuesta
        response = []
        for order in orders_db:
            # Obtener el usuario
            user = db.query(UserModel).filter(UserModel.num_doc == order.user_id).first()
            # Obtener el estado de la orden
            state_order = [
                state for state in states_order_db if state['id'] == order.status_order]
            # Obtener los detalles de la orden
            details = [
                detail for detail in details_db if detail.order_id == order.id]
            # Crear el Json de respuesta
            order_json = {
                'id': order.id,
                'user': {
                    'num_doc': user.num_doc,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active,
                },
                'status_order': state_order,
                'created_at': order.created_at,
                'details': []
            }
            for detail in details:
                # Obtener el producto
                product = db.query(ProductModel).filter(
                    ProductModel.id == detail.product_id).first()
                # Obtener la categoria
                category = next((category for category in categories_db if category['id'] == product.category_id), None)
                # Obtener el modelo
                model = db.query(ModelModel).filter(
                    ModelModel.id == product.model_id).first()
                # Obtener la marca
                brand = db.query(BrandModel).filter(
                    BrandModel.id == product.brand_id).first()
                # Obtener el estado del producto
                state_product = next((state for state in states_product_db if state['id'] == product.status_id), None)
                # Crear el Json de respuesta
                detail_json = {
                    'id': detail.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'category': category,
                        'model': {
                            'id': model.id,
                            'name': model.name,
                        },
                        'brand': {
                            'id': brand.id,
                            'name': brand.name,
                        },
                        'quantity': product.quantity,
                        'price': product.price,
                        'status_product': state_product,
                    },
                    'quantity': detail.quantity,
                }
                order_json['details'].append(detail_json)
            response.append(order_json)
        return response

@order.get('/obtenerOrdenesPorUsuario', status_code=status.HTTP_200_OK, name='USUARIO - Obtener ordenes del usuario logueado')
async def obtener_ordenes_por_usuario(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    # Obtener todas las ordenes del usuario
    orders = db.query(OrderModel).filter(OrderModel.user_id ==
                                         user[user_type]['numeroDocumento']).all()
    # Obtener todos los detalles de orden
    details_db = db.query(DetailOrderModel).all()
    # Obtener todos los productos
    products_db = db.query(ProductModel).all()
    # Obtener todas las categorias
    categories_db = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 3).all()
    categories_db = [
        {'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener todos los modelos
    models_db = db.query(ModelModel).all()
    # Obtener todas las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener todos los estados de producto
    states_product_db = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 5).all()
    states_product_db = [
        {'id': state.id_table, 'description': state.description} for state in states_product_db]
    # Obtener todos los usuarios
    users_db = db.query(UserModel).all()
    # Obtener todos los estados de orden
    states_order_db = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 4).all()
    states_order_db = [
        {'id': state.id_table, 'description': state.description} for state in states_order_db]
    
    # Crear el Json de respuesta
    response = []
    for order in orders:
        # Obtener el usuario
        user = db.query(UserModel).filter(UserModel.num_doc == order.user_id).first()
        # Obtener el estado de la orden
        state_order = [
            state for state in states_order_db if state['id'] == order.status_order]
        # Obtener los detalles de la orden
        details = [
            detail for detail in details_db if detail.order_id == order.id]
        # Crear el Json de respuesta
        order_json = {
            'id': order.id,
            'user': {
                'num_doc': user.num_doc,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'is_active': user.is_active,
            },
            'status_order': state_order,
            'created_at': order.created_at,
            'details': []
        }
        for detail in details:
            # Obtener el producto
            product = db.query(ProductModel).filter(
                ProductModel.id == detail.product_id).first()
            # Obtener la categoria
            category = [
                category for category in categories_db if category['id'] == product.category_id]
            # Obtener el modelo
            model = db.query(ModelModel).filter(
                ModelModel.id == product.model_id).first()
            # Obtener la marca
            brand = db.query(BrandModel).filter(
                BrandModel.id == product.brand_id).first()
            # Obtener el estado del producto
            state_product = [
                state for state in states_product_db if state['id'] == product.status_id]
            # Crear el Json de respuesta
            detail_json = {
                'id': detail.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'category': category,
                    'model': {
                        'id': model.id,
                        'name': model.name,
                    },
                    'brand': {
                        'id': brand.id,
                        'name': brand.name,
                    },
                    'quantity': product.quantity,
                    'price': product.price,
                    'status_product': state_product,
                },
                'quantity': detail.quantity,
            }
            order_json['details'].append(detail_json)
        response.append(order_json)
    return response

@order.post('/crearOrden', status_code=status.HTTP_201_CREATED, name='USUARIO - Crear orden')
async def crear_orden(order: OrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = OrderModel(
        user_id=user[user_type]['numeroDocumento'],
        created_at=order.created_at,
        discount=order.discount,
        status_order=1,
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return {'message': 'Orden creada exitosamente', 'data': order_db}

@order.get('/obtenerDetalleOrdenUsuario/{id}', status_code=status.HTTP_200_OK, name='USUARIO - Obtener detalle de orden por id de orden')
async def obtener_detalle_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
    if order_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
    if order_db.user_id != user[user_type]['numeroDocumento']:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='No tiene permisos para realizar esta acción')
    # Obtener todos los detalles de la orden
    details_db = db.query(DetailOrderModel).filter(
        DetailOrderModel.order_id == id).all()
    # Obtener todos los productos
    products_db = db.query(ProductModel).all()
    # Obtener todas las categorias
    categories_db = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 3).all()
    categories_db = [
        {'id': category.id_table, 'description': category.description} for category in categories_db]
    # Obtener todos los modelos
    models_db = db.query(ModelModel).all()
    # Obtener todas las marcas
    brands_db = db.query(BrandModel).all()
    # Obtener todos los estados de producto
    states_product_db = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 5).all()
    states_product_db = [
        {'id': state.id_table, 'description': state.description} for state in states_product_db]
    # Crear el Json de respuesta
    response = []
    for detail in details_db:
        # Obtener el producto
        product = db.query(ProductModel).filter(
            ProductModel.id == detail.product_id).first()
        # Obtener la categoria
        category = [
            category for category in categories_db if category['id'] == product.category_id]
        # Obtener el modelo
        model = db.query(ModelModel).filter(
            ModelModel.id == product.model_id).first()
        # Obtener la marca
        brand = db.query(BrandModel).filter(
            BrandModel.id == product.brand_id).first()
        # Obtener el estado del producto
        state_product = [
            state for state in states_product_db if state['id'] == product.status_id]
        # Crear el Json de respuesta
        detail_json = {
            'id': detail.id,
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'category': category,
                'model': {
                    'id': model.id,
                    'name': model.name,
                },
                'brand': {
                    'id': brand.id,
                    'name': brand.name,
                },
                'quantity': product.quantity,
                'price': product.price,
                'status_product': state_product,
            },
            'quantity': detail.quantity,
        }
        response.append(detail_json)
    return response


@order.post('/crearDetalleOrden', status_code=status.HTTP_201_CREATED, name='USUARIO - Crear detalle de orden')
async def crear_detalle_orden(detail_order: DetailOrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = db.query(OrderModel).filter(
        OrderModel.id == detail_order.order_id).first()
    if order_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
    if order_db.user_id != user[user_type]['numeroDocumento']:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='No tiene permisos para realizar esta acción')
    # Si la orden ya tiene un detalle con el mismo producto, se actualiza la cantidad
    detail_order_db = db.query(DetailOrderModel).filter(
        DetailOrderModel.order_id == detail_order.order_id).filter(DetailOrderModel.product_id == detail_order.product_id).first()
    if detail_order_db is not None:
        db.query(DetailOrderModel).filter(DetailOrderModel.order_id == detail_order.order_id, DetailOrderModel.product_id == detail_order.product_id).update(
            {DetailOrderModel.quantity: DetailOrderModel.quantity + detail_order.quantity})
        return detail_order_db
    else:
        # Si la orden no tiene un detalle con el mismo producto, se crea el detalle
        detail_order_db = DetailOrderModel(
            product_id=detail_order.product_id,
            quantity=detail_order.quantity,
            order_id=detail_order.order_id,
        )
        db.add(detail_order_db)
        return {'message': 'Detalle de orden creado exitosamente', 'data': detail_order_db}

@order.put('/aprobarOrden/{id}', status_code=status.HTTP_202_ACCEPTED, name='USUARIO - Aprobar orden')
async def aprobar_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    products_without_stock = []
    if user_type != user_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1:
                #!VERIFICAMOS SI HAY STOCK DE TODOS LOS PRODUCTOS QUE SE PIDIERON PARA PODER APROBAR LA ORDEN
                detail_order = db.query(DetailOrderModel).filter(
                    DetailOrderModel.order_id == id).all()
                for detail in detail_order:
                    product_db = db.query(ProductModel).filter(
                        ProductModel.id == detail.product_id).first()
                    if product_db.quantity < detail.quantity:
                        #!ALMACENAMOS EN UNA LISTA LOS PRODUCTOS QUE NO TIENEN STOCK SUFICIENTE
                        products_without_stock.append(product_db.name + '\n')
                if len(products_without_stock) > 0:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No hay stock suficiente de los siguientes productos: {}'.format(
                        products_without_stock).replace('[', '').replace(']', ''))
                #!SI HAY STOCK SUFICIENTE DE TODOS LOS PRODUCTOS, SE ACTUALIZA EL ESTADO DE LA ORDEN A APROBADA
                db.query(OrderModel).filter(OrderModel.id == id).update(
                    {OrderModel.status_order: 2})
                return {'message': 'Orden aprobada exitosamente'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='El estado de la orden no permite realizar esta acción')


@order.put('/anularOrdenCliente/{id}', status_code=status.HTTP_202_ACCEPTED, name='CLIENTE - Anular orden')
async def anular_orden_cliente(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1 or order_db.status_order == 2:
                db.query(OrderModel).filter(OrderModel.id == id).update(
                    {OrderModel.status_order: 5})
                db.commit()
                db.refresh(order_db)
                return {'message': 'Orden anulada exitosamente'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='El estado de la orden no permite realizar esta acción')


@order.put('/admin/rechazarOrden/{id}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR|TRABAJADOR - Rechazar orden')
async def rechazar_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1 or order_db.status_order == 2:
                db.query(OrderModel).filter(OrderModel.id == id).update(
                    {OrderModel.status_order: 4})
                return {'message': 'Orden rechazada exitosamente'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='El estado de la orden no permite realizar esta acción')

#! AL CREAR LA VENTA, SE ACTUALIZA EL ESTADO DE LA ORDEN PAGADO
#! AHORA ACA TENEMOS QUE TENER LISTO Y ENTREGADO
@order.put('/admin/listoOrden/{id}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR|TRABAJADOR - Listo orden')
async def listo_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 8:
                db.query(OrderModel).filter(OrderModel.id == id).update(
                    {OrderModel.status_order: 9})
                return {'message': 'Orden lista exitosamente'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='El estado de la orden no permite realizar esta acción')


@order.put('/admin/entregadoOrden/{id}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR|TRABAJADOR - Entregado orden')
async def entregado_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 9:
                db.query(OrderModel).filter(OrderModel.id == id).update(
                    {OrderModel.status_order: 3})
                return {'message': 'Orden entregada exitosamente'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='El estado de la orden no permite realizar esta acción')
