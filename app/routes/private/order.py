from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.order import Order as OrderModel
from app.schemas.order import OrderPost, OrderPut
from app.models.detail_order import DetailOrder as DetailOrderModel
from app.schemas.detail_order import DetailOrderPost
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

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

@order.put('/actualizarEstadoOrdenCliente/{id}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_estado_orden(id: int, order: OrderPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            if order.status_order == 5 or order.status_order == 6:
                order_db.status_order = order.status_order
                db.commit()
                db.refresh(order_db)
                return order_db
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no es válido')
            
@order.put('/actualizarEstadoOrden/{id}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_estado_orden(id: int, order: OrderPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_db = db.query(OrderModel).filter(OrderModel.id == id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La orden no existe')
        else:
            #!EL ESTADO FUE REGISTRADO CON ESTADO 1, EL FLUJO DE LA ORDEN ES EL SIGUIENTE:
            #!1: PENDIENTE -> PUEDE CAMBIAR A 2: APROBADO O 4: RECHAZADO
            #!2: APROBADO -> PUEDE CAMBIAR A 8: PAGADO O 5: ANULADO
            #!8: PAGADO -> PUEDE CAMBIAR A 9: LISTO
            #!9: LISTO -> PUEDE CAMBIAR A 3: ENTREGADO
            #!3: ENTREGADO -> PUEDE CAMBIAR A 6: DEVOLUCIÓN
            #!6: DEVOLUCIÓN -> PUEDE CAMBIAR A 7: REEMBOLSO
            #!7: REEMBOLSO -> PUEDE CAMBIAR A 5: ANULADO
            if order_db.status_order == 1:
                if order.status_order == 2 or order.status_order == 4:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser aprobado o rechazado')
            elif order_db.status_order == 2:
                if order.status_order == 8 or order.status_order == 5:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser pagado o anulado')
            elif order_db.status_order == 8:
                if order.status_order == 9:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser listo')
            elif order_db.status_order == 9:
                if order.status_order == 3:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser entregado')
            elif order_db.status_order == 3:
                if order.status_order == 6:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser devuelto')
            elif order_db.status_order == 6:
                if order.status_order == 7:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser reembolsado')
            elif order_db.status_order == 7:
                if order.status_order == 5:
                    order_db.status_order = order.status_order
                    db.commit()
                    db.refresh(order_db)
                    return order_db
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El pedido solo puede ser anulado')
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El estado de la orden no es válido')
            
#!DETALLE ORDENES

@order.get('/obtenerDetalleOrdenUsuario/{id}', status_code=status.HTTP_200_OK)
async def obtener_detalle_orden(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    #!Verificar que el usuario sea el dueño de la orden
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