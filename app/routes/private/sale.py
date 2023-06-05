from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.schemas.sale import SalePost
from app.models.sale import Sale as SaleModel
from app.models.order import Order as OrderModel
from app.models.product import Product as ProductModel
from app.models.detail_order import DetailOrder as DetailOrderModel
from datetime import datetime
from app.models.order_guide import OrderGuide as OrderGuideModel
from app.models.detail_order_guide import DetailOrderGuide as DetailOrderGuideModel
from app.models.sn import Sn as SerialNumberModel

sale = APIRouter()

@sale.get('/listarVentas', status_code=status.HTTP_200_OK)
async def get_sales(user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        sales = db.query(SaleModel).all()
        return sales
    
@sale.get('/listarVenta/{id}', status_code=status.HTTP_200_OK)
async def get_sale(id:int, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        sale = db.query(SaleModel).filter(SaleModel.id == id).first()
        return sale
    
@sale.get('/listarVentasUsuario', status_code=status.HTTP_200_OK)
async def get_sales_user(user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    sales = db.query(SaleModel).filter(SaleModel.user_id == user[user_type]['numeroDocumento']).all()
    return sales

@sale.post('/registrarVenta', status_code=status.HTTP_201_CREATED)
async def create_sale(codigo_pago:str, sale: SalePost, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        #!SELECCIONAR LA ORDEN Y VERIFICAR EL ESTADO QUE TENGA ESTADO 8
        order_db = db.query(OrderModel).filter(OrderModel.id == sale.order_id).first()
        if order_db is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontró la orden')
        if order_db.state_id != 8:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La orden no se encuentra en estado de pago')
        #!REGISTRAR LA VENTA
        #!OBTENER EL PRECIO DE LOS PRODUCTOS DEL TODOS LOS DETALLES DE LA ORDEN
        #!OBTENER EL TOTAL DE LA ORDEN
        detail_orders = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == sale.order_id).all()
        total = 0.0
        for detail_order in detail_orders:
            product_db = db.query(ProductModel).filter(ProductModel.id == detail_order.product_id).first()
            total += product_db.price * detail_order.quantity
            #!ACTUALIZAR EL STOCK DE LOS PRODUCTOS
            product_db.stock = product_db.stock - detail_order.quantity
            db.add(product_db)
            db.commit()
            db.refresh(product_db)
        #!APLICAR DESCUENTO
        total = total - (total * order_db.discount)
        sale_db = SaleModel(
            order_id = sale.order_id,
            user_id = user[user_type]['numeroDocumento'],
            code_payment = codigo_pago,
            created_at = sale.created_at,
            total = total
        )
        db.add(sale_db)
        db.commit()
        db.refresh(sale_db)
        #!ACTUALIZAR EL ESTADO DE LA ORDEN
        order_db.state_id = 9
        db.add(order_db)
        db.commit()
        db.refresh(order_db)
        #!REGISTRAR LA GUIA DE ORDEN
        order_guide_db = OrderGuideModel(
            order_id = sale.order_id,
            created_at = datetime.now()
        )
        db.add(order_guide_db)
        db.commit()
        db.refresh(order_guide_db)
        #!REGISTRAR LOS DETALLES DE LA GUIA DE ORDEN
        for detail_order in detail_orders:
            #!OBTENER 1 SERIAL NUMBER POR CADA PRODUCTO UNITARIAMENTE
            serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.product_id == detail_order.product_id).first()
            #!actualizar estado a 2 y el departure_at
            serial_number_db.state_id = 2
            serial_number_db.departure_at = datetime.now()
            db.add(serial_number_db)
            db.commit()
            db.refresh(serial_number_db)
            detail_order_guide_db = DetailOrderGuideModel(
                sn_id = serial_number_db.id,
                order_guide_id = order_guide_db.id
            )
            db.add(detail_order_guide_db)
            db.commit()
            db.refresh(detail_order_guide_db)
        return sale_db
    
@sale.get('/listarGuiaOrden/{id}', status_code=status.HTTP_200_OK)
async def get_order_guide(id:int, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_guide = db.query(OrderGuideModel).filter(OrderGuideModel.id == id).first()
        return order_guide
    
@sale.get('/listarGuiasOrden', status_code=status.HTTP_200_OK)
async def get_order_guides(user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        order_guides = db.query(OrderGuideModel).all()
        return order_guides
    
@sale.get('/listarGuiasOrdenUsuario', status_code=status.HTTP_200_OK)
async def get_order_guides_user(user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    order_guides = db.query(OrderGuideModel).filter(OrderGuideModel.user_id == user[user_type]['numeroDocumento']).all()
    return order_guides

@sale.get('/listarDetalleGuiaOrden/{id}', status_code=status.HTTP_200_OK)
async def get_detail_order_guide(id:int, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        detail_order_guide = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == id).all()
        return detail_order_guide
    
@sale.get('/listarDetalleGuiasOrdenUsuario/{id}', status_code=status.HTTP_200_OK)
async def get_order_guides_user(id:int, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    order_guides = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == id).filter(DetailOrderGuideModel.user_id == user[user_type]['numeroDocumento']).all()
    return order_guides