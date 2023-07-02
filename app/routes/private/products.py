from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.product import Product as ProductModel
from app.schemas.product import ProductPost, ProductPut
from app.models.sn import SerialNumber as SerialNumberModel
from app.schemas.sn import SerialNumberPost
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel
from app.models.user import User as UserModel
from app.models.supplier import Supplier as SupplierModel
from app.models.movement import Movement as MovementModel
from app.models.purchase_order import PurchaseOrder as PurchaseOrderModel

products = APIRouter()


@products.get('/estadosProductos', status_code=status.HTTP_200_OK, name='Estados de los productos')
async def estados_pedidos(db: Session = Depends(get_db)):
    estados = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 5).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]


@products.get('/admin/obtenerProductos', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener productos')
async def obtener_productos(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description}
                      for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description}
                   for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener productos
        products_db = db.query(ProductModel).all()

        # Crear el Json de respuesta
        response = []

        for product in products_db:
            category = next(
                (item for item in categories if item['id'] == product.category_id), None)
            brand = next(
                (item for item in brands if item.id == product.brand_id), None)
            model = next(
                (item for item in models if item.id == product.model_id), None)
            estado = next(
                (item for item in estados if item['id'] == product.status_id), None)
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
async def obtener_productos_paginacion(page: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description}
                      for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description}
                   for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener productos
        products_db = db.query(ProductModel).offset(page).limit(10).all()

        # Crear el Json de respuesta
        response = []

        for product in products_db:
            category = next(
                (item for item in categories if item['id'] == product.category_id), None)
            brand = next(
                (item for item in brands if item.id == product.brand_id), None)
            model = next(
                (item for item in models if item.id == product.model_id), None)
            estado = next(
                (item for item in estados if item['id'] == product.status_id), None)
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
async def obtener_producto(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener categorias
        categories = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 3).all()
        categories = [{'id': category.id_table, 'description': category.description}
                      for category in categories]
        # Obtener estados de los productos
        estados = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        estados = [{'id': estado.id_table, 'description': estado.description}
                   for estado in estados]
        # Obtener marcas
        brands = db.query(BrandModel).all()
        # Obtener modelos
        models = db.query(ModelModel).all()
        # Obtener producto
        product = db.query(ProductModel).filter(ProductModel.id == id).first()

        # Crear el Json de respuesta
        category = next(
            (item for item in categories if item['id'] == product.category_id), None)
        brand = next(
            (item for item in brands if item.id == product.brand_id), None)
        model = next(
            (item for item in models if item.id == product.model_id), None)
        estado = next(
            (item for item in estados if item['id'] == product.status_id), None)
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        product_db = ProductModel(
            name=product.name,
            description=product.description,
            path_image=product.path_image,
            quantity=0,
            discount=product.discount,
            price=product.price,
            warranty=product.warranty,
            category_id=product.category_id,
            brand_id=product.brand_id,
            model_id=product.model_id,
            status_id=1,
            ranking=0
        )
        db.add(product_db)
        db.commit()
        db.refresh(product_db)
        return product_db


@products.put('/admin/actualizarProducto/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Actualizar producto')
async def actualizar_producto(id: int, product: ProductPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        product_db = db.query(ProductModel).filter(
            ProductModel.id == id).first()
        if product_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='No existe el producto')
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
    estados = db.query(TableOfTablesModel).filter(
        TableOfTablesModel.id == 6).all()
    return [{'id': estado.id_table, 'description': estado.description} for estado in estados]


@products.get('/admin/obtenerSerialNumbers', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener serial numbers')
async def obtener_serial_numbers(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    User_type = list(user.keys())[0]
    if User_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener serial numbers
        serial_numbers_db = db.query(SerialNumberModel).all()
        # Obtener categorias
        categories_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 3).all()
        categories_db = [{'id': category.id_table, 'description': category.description}
                         for category in categories_db]
        # Obtener estados de los productos
        estados_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        estados_db = [{'id': estado.id_table, 'description': estado.description}
                      for estado in estados_db]
        # Obtener marcas
        brands_db = db.query(BrandModel).all()
        # Obtener modelos
        models_db = db.query(ModelModel).all()
        # Estado de los productos
        estados_productos = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 5).all()
        estados_productos = [{'id': estado.id_table, 'description': estado.description}
                              for estado in estados_productos]

        # Crear el Json de respuesta
        response = []

        for serial_number_db in serial_numbers_db:
            # Obtener el producto
            products_db = db.query(ProductModel).filter(
                ProductModel.id == serial_number_db.product_id).first()
            # Obtener la marca
            category = next(
                (item for item in categories_db if item['id'] == products_db.category_id), None)
            brand = next(
                (item for item in brands_db if item.id == products_db.brand_id), None)
            model = next(
                (item for item in models_db if item.id == products_db.model_id), None)
            estado = next(
                (item for item in estados_productos if item['id'] == products_db.status_id), None)
            # Obtener el proveedor
            supplier_db = db.query(SupplierModel).filter(
                SupplierModel.num_doc == serial_number_db.supplier_id).first()
            # Obtener el usuario
            user_db = db.query(UserModel).filter(
                UserModel.num_doc == serial_number_db.user_id).first()
            # Obtener el estado
            estado_sn = [estado for estado in estados_db if estado['id'] == serial_number_db.status_id]
            # Obtener Orden de Compra
            purchase_order_db = db.query(PurchaseOrderModel).filter(
                PurchaseOrderModel.id == serial_number_db.oc_id).first()
            
            # Crear el Json de respuesta
            serial_numer_json = {
                'id': serial_number_db.sn_id,
                'product': {
                    'id': products_db.id,
                    'name': products_db.name,
                    'description': products_db.description,
                    'category': category,
                    'brand': brand,
                    'model': model,
                    'estado': estado,
                    'ranking': products_db.ranking,
                },
                'supplier': {
                    'razon_social': supplier_db.num_doc,
                    'name': supplier_db.name,
                    'doc_representante': supplier_db.num_doc_representative,
                    'name_representative': supplier_db.name_representative,
                    'email': supplier_db.email,
                    'phone': supplier_db.phone,
                    'estado': supplier_db.status,
                },
                'user': {
                    'num_doc': user_db.num_doc,
                    'full_name': user_db.full_name,
                    'username': user_db.username,
                    'email': user_db.email,
                    'is_active': user_db.is_active
                },
                'status': estado_sn,
                'oc': purchase_order_db,
                'entrance_at': serial_number_db.entrance_at,
                'departure_at': serial_number_db.departure_at,
            }
            response.append(serial_numer_json)
        return response
    
@products.get('/admin/obtenerSerialNumbersProduct/{product_id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener los numeros de serie de un producto')
async def obtener_serial_numbers_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    else:
        # Comprobar si existe el producto
        product_db = db.query(ProductModel).filter(
            ProductModel.id == product_id).first()
        if not product_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No existe el producto')
        # Obtener serial numbers de un producto
        serial_numbers_db = db.query(SerialNumberModel).filter(
            SerialNumberModel.product_id == product_id).all()
        # Obtener estados de los numeros de serie
        estados_db = db.query(TableOfTablesModel).filter(
            TableOfTablesModel.id == 6).all()
        estados_db = [{'id': estado.id_table, 'description': estado.description}
                        for estado in estados_db]
        # Crear el Json de respuesta
        response = []

        for serial_number_db in serial_numbers_db:
            # Obtener el proveedor
            supplier_db = db.query(SupplierModel).filter(
                SupplierModel.num_doc == serial_number_db.supplier_id).first()
            # Obtener el usuario
            user_db = db.query(UserModel).filter(
                UserModel.num_doc == serial_number_db.user_id).first()
            # Obtener el estado
            estado_db = [estado for estado in estados_db if estado['id'] == serial_number_db.status_id]
            # Obtener Orden de Compra
            purchase_order_db = db.query(PurchaseOrderModel).filter(
                PurchaseOrderModel.id == serial_number_db.oc_id).first()

            # Crear el Json de respuesta
            serial_numer_json = {
                'id': serial_number_db.sn_id,
                'supplier': {
                    'razon_social': supplier_db.num_doc,
                    'name': supplier_db.name,
                    'doc_representante': supplier_db.num_doc_representative,
                    'name_representative': supplier_db.name_representative,
                    'email': supplier_db.email,
                    'phone': supplier_db.phone,
                    'estado': supplier_db.status,
                },
                'user': {
                    'num_doc': user_db.num_doc,
                    'full_name': user_db.full_name,
                    'username': user_db.username,
                    'email': user_db.email,
                    'is_active': user_db.is_active
                },
                'status': estado_db,
                'oc': purchase_order_db,
                'entrance_at': serial_number_db.entrance_at,
                'departure_at': serial_number_db.departure_at,
            }
            response.append(serial_numer_json)
        return response

@products.post('/admin/crearSerialNumber', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR|TRABAJADOR - Crear serial number')
async def crear_serial_number(serial_number: SerialNumberPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    serial_number_exist = db.query(SerialNumberModel).filter(
        SerialNumberModel.sn_id == serial_number.sn_id).first()
    if serial_number_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='El numero de serie ya fue registrado')
    serial_number_db = SerialNumberModel(
        sn_id=serial_number.sn_id,
        product_id=serial_number.product_id,
        supplier_id=serial_number.supplier_id,
        user_id=user[user_type]['numeroDocumento'],
        status_id=1,
        oc_id=serial_number.oc_id,
        entrance_at=datetime.now()
    )
    db.add(serial_number_db)
    db.commit()
    db.refresh(serial_number_db)
    #!ACTUALIZAR CANTIDAD DE PRODUCTOS
    product_db = db.query(ProductModel).filter(
        ProductModel.id == serial_number.product_id).first()
    product_db.quantity = product_db.quantity + 1
    db.commit()
    db.refresh(product_db)
    #!CREAR MOVIMIENTO
    movement_db = MovementModel(
        sn_id=serial_number_db.sn_id,
        user_id=user[user_type]['numeroDocumento'],
        created_at=datetime.now(),
        type_id=1,
    )
    db.add(movement_db)
    db.commit()
    db.refresh(movement_db)
    return serial_number_db