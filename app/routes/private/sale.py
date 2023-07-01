from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.schemas.sale import SalePost
from app.models.sale import Sale as SaleModel
from app.models.order import Order as OrderModel
from app.models.detail_order import DetailOrder as DetailOrderModel
from datetime import datetime
from app.models.order_guide import OrderGuide as OrderGuideModel
from app.models.detail_order_guide import DetailOrderGuide as DetailOrderGuideModel
from app.models.user import User as UserModel
from app.models.product import Product as ProductModel
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.sn import SerialNumber as SerialNumberModel
from app.models.movement import Movement as MovementModel

sale = APIRouter()

@sale.get('/admin/listarVentas', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Lista todas las ventas')
async def get_sales(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []
        # Obtener todas las ventas
        sales = db.query(SaleModel).all()
        # Recorrer las ventas
        for sale in sales:
            # Obtener las Marcas y Modelos
            brands = db.query(BrandModel).all()
            models = db.query(ModelModel).all()

            # Obtener categorias de la tabla de tablas
            categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
            categories = sorted(categories, key=lambda x: x.id_table)
            categories = [{'id': category.id_table, 'description': category.description} for category in categories]

            # Obtener documentos de la tabla de tablas
            documents = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 1).all()
            documents = sorted(documents, key=lambda x: x.id_table)
            documents = [{'id': document.id_table, 'description': document.description} for document in documents]

            # Obtener el usuario
            user_db = db.query(UserModel).filter(UserModel.num_doc == sale.user_id).first()
            # Obtener la orden
            order_db = db.query(OrderModel).filter(OrderModel.id == sale.order_id).first()
            # Obtener los detalles de la orden
            detail_orders = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == order_db.id).all()
            # Obtener los productos
            products = []
            for detail_order in detail_orders:
                product = db.query(ProductModel).filter(ProductModel.id == detail_order.product_id).first()
                products.append(product)

            # Crear el Json de la venta
            sale_json = {
                'id': sale.id,
                'order_id': {
                    'id': order_db.id,
                    'created_at': order_db.created_at,
                    'discount': order_db.discount,
                    'status_order': order_db.status_order,
                    'detail_orders': [
                        {
                            'id': detail_order.id,
                            'product_id': {
                                'id': product.id,
                                'name': product.name,
                                'description': product.description,
                                'model_id': {
                                    'id': product.model_id,
                                    'name': [model.name for model in models if model.id == product.model_id][0]
                                },
                                'brand_id': {
                                    'id': product.brand_id,
                                    'name': [brand.name for brand in brands if brand.id == product.brand_id][0]
                                },
                                'category_id': {
                                    'id': product.category_id,
                                    'description': [category['description'] for category in categories if category['id'] == product.category_id][0]
                                },
                            },
                            'quantity': detail_order.quantity,
                        } for detail_order, product in zip(detail_orders, products)
                    ] if detail_orders else []
                },
                'user_id': {
                    'num_doc': user_db.num_doc,
                    'type_doc': {
                        'id': user_db.type_doc,
                        'description': [document['description'] for document in documents if document['id'] == user_db.type_doc][0]
                    },
                    'full_name': user_db.full_name,
                    'email': user_db.email,
                },
                'code_payment': sale.code_payment,
                'created_at': sale.created_at,
                'total': sale.total
            }
            # Agregar la venta al Json de respuesta
            response.append(sale_json)
        return response
    
    
@sale.get('/admin/listarVenta/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Lista una venta por id')
async def get_sale(id:int, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []
        # Obtener todas las ventas
        sale = db.query(SaleModel).filter(SaleModel.id == id).first()
        # Recorrer las ventas
        # Obtener las Marcas y Modelos
        brands = db.query(BrandModel).all()
        models = db.query(ModelModel).all()

        # Obtener categorias de la tabla de tablas
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = sorted(categories, key=lambda x: x.id_table)
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]

        # Obtener documentos de la tabla de tablas
        documents = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 1).all()
        documents = sorted(documents, key=lambda x: x.id_table)
        documents = [{'id': document.id_table, 'description': document.description} for document in documents]

        # Obtener el usuario
        user_db = db.query(UserModel).filter(UserModel.num_doc == sale.user_id).first()
        # Obtener la orden
        order_db = db.query(OrderModel).filter(OrderModel.id == sale.order_id).first()
        # Obtener los detalles de la orden
        detail_orders = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == order_db.id).all()
        # Obtener los productos
        products = []
        for detail_order in detail_orders:
            product = db.query(ProductModel).filter(ProductModel.id == detail_order.product_id).first()
            products.append(product)


        # Crear el Json de la venta
        sale_json = {
            'id': sale.id,
            'order_id': {
                'id': order_db.id,
                'created_at': order_db.created_at,
                'discount': order_db.discount,
                'status_order': order_db.status_order,
                'detail_orders': [
                    {
                        'id': detail_order.id,
                        'product_id': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'model_id': {
                                'id': product.model_id,
                                'name': [model.name for model in models if model.id == product.model_id][0]
                            },
                            'brand_id': {
                                'id': product.brand_id,
                                'name': [brand.name for brand in brands if brand.id == product.brand_id][0]
                            },
                            'category_id': {
                                'id': product.category_id,
                                'description': [category['description'] for category in categories if category['id'] == product.category_id][0]
                            },
                            'price': product.price,
                        },
                        'quantity': detail_order.quantity,
                    } for detail_order, product in zip(detail_orders, products)
                ] if detail_orders else []
            },
            'user_id': {
                'num_doc': user_db.num_doc,
                'type_doc': {
                    'id': user_db.type_doc,
                    'description': [document['description'] for document in documents if document['id'] == user_db.type_doc][0]
                },
                'full_name': user_db.full_name,
                'email': user_db.email,
            },
            'code_payment': sale.code_payment,
            'created_at': sale.created_at,
            'total': sale.total
        }
        # Agregar la venta al Json de respuesta
        response.append(sale_json)
        return response
    
@sale.get('/listarVentasUsuario', status_code=status.HTTP_200_OK, name='USUARIO - Lista las ventas del usuario logueado')
async def get_sales_user(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    # Crear el Json de respuesta
    response = []
    # Obtener todas las ventas
    sales = db.query(SaleModel).filter(SaleModel.user_id == user[user_type]['numeroDocumento']).all()
    # Recorrer las ventas
    for sale in sales:
        # Obtener las Marcas y Modelos
        brands = db.query(BrandModel).all()
        models = db.query(ModelModel).all()

        # Obtener categorias de la tabla de tablas
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = sorted(categories, key=lambda x: x.id_table)
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]

        # Obtener documentos de la tabla de tablas
        documents = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 1).all()
        documents = sorted(documents, key=lambda x: x.id_table)
        documents = [{'id': document.id_table, 'description': document.description} for document in documents]

        # Obtener el usuario
        user_db = db.query(UserModel).filter(UserModel.num_doc == sale.user_id).first()
        # Obtener la orden
        order_db = db.query(OrderModel).filter(OrderModel.id == sale.order_id).first()
        # Obtener los detalles de la orden
        detail_orders = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == order_db.id).all()
        # Obtener los productos
        products = []
        for detail_order in detail_orders:
            product = db.query(ProductModel).filter(ProductModel.id == detail_order.product_id).first()
            products.append(product)

        # Crear el Json de la venta
        sale_json = {
            'id': sale.id,
            'order_id': {
                'id': order_db.id,
                'created_at': order_db.created_at,
                'discount': order_db.discount,
                'status_order': order_db.status_order,
                'detail_orders': [
                    {
                        'id': detail_order.id,
                        'product_id': {
                            'id': product.id,
                            'name': product.name,
                            'description': product.description,
                            'model_id': {
                                'id': product.model_id,
                                'name': [model.name for model in models if model.id == product.model_id][0]
                            },
                            'brand_id': {
                                'id': product.brand_id,
                                'name': [brand.name for brand in brands if brand.id == product.brand_id][0]
                            },
                            'category_id': {
                                'id': product.category_id,
                                'description': [category['description'] for category in categories if category['id'] == product.category_id][0]
                            },
                            'price': product.price
                        },
                        'quantity': detail_order.quantity,
                    } for detail_order, product in zip(detail_orders, products)
                ] if detail_orders else []
            },
            'user_id': {
                'num_doc': user_db.num_doc,
                'type_doc': {
                    'id': user_db.type_doc,
                    'description': [document['description'] for document in documents if document['id'] == user_db.type_doc][0]
                },
                'full_name': user_db.full_name,
                'email': user_db.email,
            },
            'code_payment': sale.code_payment,
            'created_at': sale.created_at,
            'total': sale.total
        }
        # Agregar la venta al Json de respuesta
        response.append(sale_json)
    return response

#!NUEVA LOGICA DE REGISTRO DE VENTA
@sale.post('/registrarVenta', status_code=status.HTTP_201_CREATED, name='USUARIO - Registrar una venta')
async def create_sale2(sale: SalePost, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    #!SELECCIONAR LA ORDEN Y VERIFICAR EL ESTADO QUE TENGA ESTADO 2
    order_db = db.query(OrderModel).filter(OrderModel.id == sale.order_id).first()
    if order_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontró la orden')
    if order_db.status_order != 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La orden no se encuentra en aprobada')
    #!VERIFICAR QUE LA ORDEN NO TENGA UNA VENTA REGISTRADA
    sale_db = db.query(SaleModel).filter(SaleModel.order_id == sale.order_id).first()
    if sale_db is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La orden ya cuenta con una venta registrada')
    #!REGISTRAR LA VENTA
    #!OBTENER EL PRECIO DE LOS PRODUCTOS DEL TODOS LOS DETALLES DE LA ORDEN
    #!OBTENER EL TOTAL DE LA ORDEN
    detail_orders = db.query(DetailOrderModel).filter(DetailOrderModel.order_id == sale.order_id).all()
    total = 0.0
    for detail_order in detail_orders:
        product_db = db.query(ProductModel).filter(ProductModel.id == detail_order.product_id).first()
        total += product_db.price * detail_order.quantity
        #!ACTUALIZAR EL STOCK DE LOS PRODUCTOS
        product_db.quantity = product_db.quantity - detail_order.quantity
        if product_db.quantity < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'No se cuenta con los productos requeridos en el stock\nPodroducto faltante {product_db.name}.')
        db.add(product_db)
        db.commit()
        db.refresh(product_db)
    #!APLICAR DESCUENTO
    total = total - (total * order_db.discount)
    sale_db = SaleModel(
        order_id = sale.order_id,
        user_id = user[user_type]['numeroDocumento'],
        code_payment = sale.code_payment,
        created_at = sale.created_at,
        total = total
    )
    db.add(sale_db)
    db.commit()
    db.refresh(sale_db)
    #!ACTUALIZAR EL ESTADO DE LA ORDEN
    order_db.status_order = 8
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
            sn_id = serial_number_db.sn_id,
            order_guide_id = order_guide_db.id
        )
        db.add(detail_order_guide_db)
        db.commit()
        db.refresh(detail_order_guide_db)
        #!CREAR EL MOVIMIENTO DE SALIDA
        movement_db = MovementModel(
            sn_id = serial_number_db.sn_id,
            user_id = user[user_type]['numeroDocumento'],
            type_movement = 2,
            created_at = datetime.now()
        )
        db.add(movement_db)
        db.commit()
        db.refresh(movement_db)
    return sale_db


    
@sale.get('/admin/listarGuiaOrden/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener la guia de una orden por id')
async def get_order_guide(id:int, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []

        # Obtener estados de numeros de serie
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]

        # Buscar la guia de orden
        order_guide_db = db.query(OrderGuideModel).filter(OrderGuideModel.id == id).first()
        if order_guide_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontró la guia de orden')
        
        # Buscar los detalles de la guia de orden
        detail_order_guide_db = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == order_guide_db.id).all()
        
        for detail in detail_order_guide_db:
            # Buscar el serial number
            serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == detail.sn_id).first()
            # Buscar el producto
            product_db = db.query(ProductModel).filter(ProductModel.id == serial_number_db.product_id).first()
            # Buscar el estado del serial number
            estado = [estado for estado in estados if estado['id'] == serial_number_db.status_id]
            # Crear el Json de respuesta
            response.append({
                'id': serial_number_db.sn_id,
                'product': {
                    'id': product_db.id,
                    'name': product_db.name,
                    'price': product_db.price
                },
                'state': estado,
                'entrance_at': serial_number_db.entrance_at,
                'departure_at': serial_number_db.departure_at
            })
        return response

@sale.get('/admin/listarGuiasOrden', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener todas las guias de orden')
async def get_order_guides(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []

        # Obtener estados de numeros de serie
        estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
        estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]

        # Obtener estados de ordenes
        estados_order = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 4).all()
        estados_order = [{'id': estado.id_table, 'description': estado.description} for estado in estados_order]

        # Buscar las guias de orden
        order_guides_db = db.query(OrderGuideModel).all()
        for order_guide_db in order_guides_db:
            # Buscar los detalles de la guia de orden
            detail_order_guide_db = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == order_guide_db.id).all()
            # Buscar la orden de la guia de orden
            order_db = db.query(OrderModel).filter(OrderModel.id == order_guide_db.order_id).first()
            # Buscar el usuario de la orden
            user_db = db.query(UserModel).filter(UserModel.num_doc == order_db.user_id).first()
            # Crear el Json de respuesta
            response.append({
                'id': order_guide_db.id,
                'created_at': order_guide_db.created_at,
                'order': {
                    'id': order_db.id,
                    'user': {
                        'id': user_db.num_doc,
                        'full_name': user_db.full_name,
                        'email': user_db.email,
                    },
                    'created_at': order_db.created_at,
                    'status': {
                        'id': order_db.status_order,
                        'description': [estado['description'] for estado in estados_order if estado['id'] == order_db.status_order][0]
                    }
                },
                'details': []
            })

            for detail in detail_order_guide_db:
                # Buscar el serial number
                serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == detail.sn_id).first()
                # Buscar el producto
                product_db = db.query(ProductModel).filter(ProductModel.id == serial_number_db.product_id).first()
                # Buscar el estado del serial number
                estado = [estado for estado in estados if estado['id'] == serial_number_db.status_id][0]
                # Crear el Json de respuesta
                response[-1]['details'].append({
                    'id': serial_number_db.sn_id,
                    'product': {
                        'id': product_db.id,
                        'name': product_db.name,
                        'price': product_db.price
                    },
                    'state': estado,
                    'entrance_at': serial_number_db.entrance_at,
                    'departure_at': serial_number_db.departure_at
                })
        return response
    
@sale.get('/listarGuiasOrdenUsuario', status_code=status.HTTP_200_OK, name='USUARIO - Obtener todas las guias de orden del usuario logueado')
async def get_order_guides_user(user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    # Crear el Json de respuesta
    response = []

    # Obtener estados de numeros de serie
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]

    # Obtener estados de ordenes
    estados_order = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 4).all()
    estados_order = [{'id': estado.id_table, 'description': estado.description} for estado in estados_order]

    # Buscar la ordenes que le pertenecen al usuario
    order = db.query(OrderModel).filter(OrderModel.user_id == user[user_type]['numeroDocumento']).all()

    # Buscar las guia de orden de cada orden
    for o in order:
        order_guide_db = db.query(OrderGuideModel).filter(OrderGuideModel.order_id == o.id).first()
        if order_guide_db:
            # Buscar los detalles de la guia de orden
            detail_order_guide_db = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == order_guide_db.id).all()
            # Buscar el usuario de la orden
            user_db = db.query(UserModel).filter(UserModel.num_doc == o.user_id).first()
            # Crear el Json de respuesta
            response.append({
                'id': order_guide_db.id,
                'created_at': order_guide_db.created_at,
                'order': {
                    'id': o.id,
                    'user': {
                        'id': user_db.num_doc,
                        'full_name': user_db.full_name,
                        'email': user_db.email,
                    },
                    'created_at': o.created_at,
                    'status': {
                        'id': o.status_order,
                        'description': [estado['description'] for estado in estados_order if estado['id'] == o.status_order][0]
                    }
                },
                'details': []
            })

            for detail in detail_order_guide_db:
                # Buscar el serial number
                serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == detail.sn_id).first()
                # Buscar el producto
                product_db = db.query(ProductModel).filter(ProductModel.id == serial_number_db.product_id).first()
                # Buscar el estado del serial number
                estado = [estado for estado in estados if estado['id'] == serial_number_db.status_id][0]
                # Crear el Json de respuesta
                response[-1]['details'].append({
                    'id': serial_number_db.sn_id,
                    'product': {
                        'id': product_db.id,
                        'name': product_db.name,
                        'price': product_db.price
                    },
                    'state': estado,
                    'entrance_at': serial_number_db.entrance_at,
                    'departure_at': serial_number_db.departure_at
                })
    return response

@sale.get('/admin/listarDetalleGuiaOrden/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener el detalle de una guia de orden')
async def get_detail_order_guide(id:int, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    # Crear el Json de respuesta
    response = []

    # Obtener estados de numeros de serie
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]

    # Obtener detalles de la guia de orden
    detail_order_guide_db = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == id).all()

    for detail in detail_order_guide_db:
        # Buscar el serial number
        serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == detail.sn_id).first()
        # Buscar el producto
        product_db = db.query(ProductModel).filter(ProductModel.id == serial_number_db.product_id).first()
        # Buscar el estado del serial number
        estado = [estado for estado in estados if estado['id'] == serial_number_db.status_id][0]
        # Crear el Json de respuesta
        response.append({
            'id': serial_number_db.sn_id,
            'product': {
                'id': product_db.id,
                'name': product_db.name,
                'price': product_db.price
            },
            'state': estado,
            'entrance_at': serial_number_db.entrance_at,
            'departure_at': serial_number_db.departure_at
        })
    return response
    
@sale.get('/listarDetalleGuiasOrdenUsuario/{id}', status_code=status.HTTP_200_OK, name='USUARIO - Obtener el detalle de una guia de orden')
async def get_order_guides_user(id:int, user: dict = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    # Buscar la guia de orden
    order_guide_db = db.query(OrderGuideModel).filter(OrderGuideModel.id == id).first()
    if not order_guide_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro la guia de orden')
    # Buscar la orden
    order_db = db.query(OrderModel).filter(OrderModel.id == order_guide_db.order_id).first()
    # Si el usuario de la orden no es el mismo que el usuario que esta realizando la peticion, denegar el acceso
    if order_db.user_id != user[user_type]['numeroDocumento']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')

    # Crear el Json de respuesta
    response = []

    # Obtener estados de numeros de serie
    estados = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 6).all()
    estados = [{'id': estado.id_table, 'description': estado.description} for estado in estados]

    # Obtener detalles de la guia de orden
    detail_order_guide_db = db.query(DetailOrderGuideModel).filter(DetailOrderGuideModel.order_guide_id == id).all()

    for detail in detail_order_guide_db:
        # Buscar el serial number
        serial_number_db = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == detail.sn_id).first()
        # Buscar el producto
        product_db = db.query(ProductModel).filter(ProductModel.id == serial_number_db.product_id).first()
        # Buscar el estado del serial number
        estado = [estado for estado in estados if estado['id'] == serial_number_db.status_id][0]
        # Crear el Json de respuesta
        response.append({
            'id': serial_number_db.sn_id,
            'product': {
                'id': product_db.id,
                'name': product_db.name,
                'price': product_db.price
            },
            'state': estado,
            'entrance_at': serial_number_db.entrance_at,
            'departure_at': serial_number_db.departure_at
        })
    return response
