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
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel
from app.models.user import User as UserModel

products = APIRouter()

@products.get('/estadosProductos', status_code=status.HTTP_200_OK, name='Estados de los productos')
async def estados_pedidos(db: Session = Depends(get_db)):
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]

@products.get('/admin/obtenerProductos', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener productos')
async def obtener_productos(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener productos
        products = db.query(ProductModel).all()

        # Crear el Json de respuesta
        response = []

        for product in products:
            category = next((item for item in categories if item['id'] == product.category_id), None)
            brand = next((item for item in brands if item.id == product.brand_id), None)
            model = next((item for item in models if item.id == product.model_id), None)
            estado = next((item for item in estados if item['id'] == product.status_id), None)
            response.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'path_image': product.path_image,
                'quantity': product.quantity,
                'discount': product.discount,
                'price': product.price,
                'warranty': product.warranty,
                'category': category,
                'brand': brand,
                'model': model,
                'estado': estado,
                'ranking': product.ranking
            })
        return response

    
@products.get('/admin/obtenerProductosPaginacion', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener productos por paginacion')
async def obtener_productos_paginacion(page:int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener productos
        products = db.query(ProductModel).offset(page).limit(10).all()
        
        # Crear el Json de respuesta
        response = []

        for product in products:
            category = next((item for item in categories if item['id'] == product.category_id), None)
            brand = next((item for item in brands if item.id == product.brand_id), None)
            model = next((item for item in models if item.id == product.model_id), None)
            estado = next((item for item in estados if item['id'] == product.status_id), None)
            response.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'path_image': product.path_image,
                'quantity': product.quantity,
                'discount': product.discount,
                'price': product.price,
                'warranty': product.warranty,
                'category': category,
                'brand': brand,
                'model': model,
                'estado': estado,
                'ranking': product.ranking
            })
        return response

@products.get('/admin/obtenerProducto/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener producto')
async def obtener_producto(id:int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener producto
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        
        # Crear el Json de respuesta
        category = next((item for item in categories if item['id'] == product.category_id), None)
        brand = next((item for item in brands if item.id == product.brand_id), None)
        model = next((item for item in models if item.id == product.model_id), None)
        estado = next((item for item in estados if item['id'] == product.status_id), None)
        response = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'path_image': product.path_image,
            'quantity': product.quantity,
            'discount': product.discount,
            'price': product.price,
            'warranty': product.warranty,
            'category': category,
            'brand': brand,
            'model': model,
            'estado': estado,
            'ranking': product.ranking
        }
        return response
    
@products.post('/admin/crearProducto', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR|TRABAJADOR - Crear producto')
async def crear_producto(product: ProductPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
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
    
@products.put('/admin/actualizarProducto/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Actualizar producto')
async def actualizar_producto(id:int, product: ProductPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
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
        
@products.get('/estadosSerialNumbers', status_code=status.HTTP_200_OK, name='Obtener estados de los serial numbers')
async def estados_serial_numbers(db: Session = Depends(get_db)):
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]

@products.get('/admin/obtenerSerialNumbers', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener serial numbers')
async def obtener_serial_numbers(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener serial numbers
        serial_numbers = db.query(SerialNumberModel).all()
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener productos
        products = db.query(ProductModel).all()
        # Obtener usuarios
        users = db.query(UserModel).all()

        # Crear el Json de respuesta
        response = []

        for serial_number in serial_numbers:
            # Obtener el usuario del serial_number
            user = db.query(UserModel).filter(UserModel.num_doc == serial_number.user_id).first()
            # Obtener el traja
            

@products.post('/crearSerialNumber', status_code=status.HTTP_201_CREATED)
async def crear_serial_number(serial_number: SerialNumberPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    serial_number_exist = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == serial_number.sn_id).first()
    if serial_number_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El numero de serie ya fue registrado')
    serial_number_db = SerialNumberModel(
        sn_id = serial_number.sn_id,
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