from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.product import Product as ProductModel
from app.schemas.product import ProductPost, ProductPut
from app.models.sn import SerialNumber as SerialNumberModel
from app.schemas.sn import SerialNumberPost
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

products = APIRouter()

@products.get('/estadosProductos')
async def estados_pedidos(db: Session = Depends(get_db)):
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]

@products.get('/obtenerProductos')
async def obtener_productos(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        products = db.query(ProductModel).all()
        return products

@products.get('/obtenerProductosPaginacion')
async def obtener_productos_paginacion(page:int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        products = db.query(ProductModel).offset(page).limit(10).all()
        return products

@products.get('/obtenerProducto/{id}')
async def obtener_producto(id:int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        return product
    
@products.post('/crearProducto')
async def crear_producto(product: ProductPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        product_db = ProductModel(
            name = product.name,
            description = product.description,
            path_image = product.path_image,
            quantity = 0,
            discount = product.discount,
            price = product.price,
            warranty = product.warranty,
            category_id = product.category_id,
            brand_id = product.brand_id,
            model_id = product.model_id,
            status_id = 1,
            ranking = 0
        )
        db.add(product_db)
        db.commit()
        db.refresh(product_db)
        return product_db
    
@products.put('/actualizarProducto/{id}')
async def actualizar_producto(id:int, product: ProductPut, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        product_db = db.query(ProductModel).filter(ProductModel.id == id).first()
        if product_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el producto')
        else:
            product_db.name = product.name
            product_db.description = product.description
            product_db.path_image = product.path_image
            product_db.quantity = product.quantity
            product_db.discount = product.discount
            product_db.price = product.price
            product_db.warranty = product.warranty
            product_db.category_id = product.category_id
            product_db.brand_id = product.brand_id
            product_db.model_id = product.model_id
            product_db.status_id = product.status_id
            product_db.ranking = product.ranking
            db.commit()
            db.refresh(product_db)
            return product_db
        
@products.get('/estadosSerialNumbers')
async def estados_serial_numbers(db: Session = Depends(get_db)):
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]

@products.get('/obtenerSerialNumbers')
async def obtener_serial_numbers(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        serial_numbers = db.query(SerialNumberModel).all()
        return serial_numbers

@products.post('/crearSerialNumber')
async def crear_serial_number(serial_number: SerialNumberPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        serial_number_db = SerialNumberModel(
            serial_number = serial_number.serial_number,
            product_id = serial_number.product_id,
            supplier_id = serial_number.supplier_id,
            user_id = user[user_type]['numeroDocumento'],
            status_id = 1,
            entrance_at = datetime.now()
        )
        #!ACTUALIZAR CANTIDAD DE PRODUCTOS
        product_db = db.query(ProductModel).filter(ProductModel.id == serial_number.product_id).first()
        product_db.quantity = product_db.quantity + 1
        db.add(serial_number_db)
        db.commit()
        db.refresh(serial_number_db)
        return serial_number_db