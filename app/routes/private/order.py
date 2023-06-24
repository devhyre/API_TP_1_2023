from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.order import Order as OrderModel
from app.schemas.order import OrderPost, OrderPut
from app.models.detail_order import DetailOrder as DetailOrderModel
from app.schemas.detail_order import DetailOrderPost
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.product import Product as ProductModel

order = APIRouter()

@order.get('/listadoEstadosOrden', status_code=status.HTTP_200_OK)
async def listar_estados_orden(db: Session = Depends(get_db)):
    states = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 4).all()
    return [{'id': state.id_table, 'description': state.description} for state in states]

@order.get('/obtenerOrdenes', status_code=status.HTTP_200_OK)
async def obtener_ordenes(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        orders = db.query(OrderModel).all()
        return orders
    
@order.get('/obtenerOrdenesPorUsuario', status_code=status.HTTP_200_OK)
async def obtener_ordenes_por_usuario(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    orders = db.query(OrderModel).filter(OrderModel.user_id == user[user_type]['numeroDocumento']).all()
    return orders

@order.post('/crearOrden', status_code=status.HTTP_201_CREATED)
async def crear_orden(order: OrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = OrderModel(
        user_id = user[user_type]['numeroDocumento'],
        created_at = order.created_at,
        discount = order.discount,
        status_order = 1,
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

@order.get('/obtenerDetalleOrdenUsuario/{id}', status_code=status.HTTP_200_OK)
async def obtener_detalle_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
    if order_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
    else:
        if user_type == 'client':
            if order_db.user_id != user[user_type]['numeroDocumento']:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
            else:
                detail_order = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == id).all()
                return detail_order
        else:
            detail_order = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == id).all()
            return detail_order
        
@order.post('/crearDetalleOrden', status_code=status.HTTP_201_CREATED)
async def crear_detalle_orden(detail_order: DetailOrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    order_db = db.query(OrderModel).filter(OrderModel.id == detail_order.order_id).first()
    if order_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
    else:
        if user_type == 'client':
            if order_db.user_id != user[user_type]['numeroDocumento']:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
            else:
                detail_order_db = DetailOrderModel(
                    product_id = detail_order.product_id,
                    quantity = detail_order.quantity,
                    order_id = detail_order.order_id,
                )
                db.add(detail_order_db)
                db.commit()
                db.refresh(detail_order_db)
                return detail_order_db
        else:
            detail_order_db = DetailOrderModel(
                product_id = detail_order.product_id,
                quantity = detail_order.quantity,
                order_id = detail_order.order_id,
            )
            db.add(detail_order_db)
            db.commit()
            db.refresh(detail_order_db)
            return detail_order_db
        
@order.put('/aprobarOrden/{id}', status_code=status.HTTP_202_ACCEPTED)
async def aprobar_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    products_without_stock = []
    if user_type != user_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1:
                #!VERIFICAMOS SI HAY STOCK DE TODOS LOS PRODUCTOS QUE SE PIDIERON PARA PODER APROBAR LA ORDEN
                detail_order = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == id).all()
                for detail in detail_order:
                    product_db = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
                    if product_db.quantity < detail.quantity:
                        #!ALMACENAMOS EN UNA LISTA LOS PRODUCTOS QUE NO TIENEN STOCK SUFICIENTE
                        products_without_stock.append(product_db.name + '\n')
                if len(products_without_stock) > 0:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No hay stock suficiente de los siguientes productos: {}'.format(products_without_stock).replace('[', '').replace(']', ''))
                #!SI HAY STOCK SUFICIENTE DE TODOS LOS PRODUCTOS, SE ACTUALIZA EL ESTADO DE LA ORDEN A APROBADA
                order_db.status_order = 2
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no permite realizar esta acción')

@order.put('/anularOrdenCliente/{id}', status_code=status.HTTP_202_ACCEPTED)
async def anular_orden_cliente(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1 or order_db.status_order == 2:
                order_db.status_order = 5
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no permite realizar esta acción')
            
@order.put('/rechazarOrden/{id}', status_code=status.HTTP_202_ACCEPTED)
async def rechazar_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 1 or order_db.status_order == 2:
                order_db.status_order = 4
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no permite realizar esta acción')
            
#! AL CREAR LA VENTA, SE ACTUALIZA EL ESTADO DE LA ORDEN PAGADO
#! AHORA ACA TENEMOS QUE TENER LISTO Y ENTREGADO

@order.put('/listoOrden/{id}', status_code=status.HTTP_202_ACCEPTED)
async def listo_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 8:
                order_db.status_order = 9
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no permite realizar esta acción')
            
@order.put('/entregadoOrden/{id}', status_code=status.HTTP_202_ACCEPTED)
async def entregado_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order_db.status_order == 9:
                order_db.status_order = 3
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no permite realizar esta acción')