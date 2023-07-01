from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.purchase_order import PurchaseOrder as PurchaseOrderModel
from app.models.detail_purchase_order import DetailPurchaseOrder as DetailPurchaseOrderModel
from app.models.supplier import Supplier as SupplierModel
from app.models.worker import Worker as WorkerModel
from app.models.product import Product as ProductModel
from app.models.brand import Brand as BrandModel
from app.models.model import Model as ModelModel
from app.models.user import User as UserModel
from app.schemas.purchase_order import PurchaseOrderPost
from app.schemas.detail_purchase_order import DetailPurchaseOrderPost, DetailPurchaseOrderPut

purchase_order_router = APIRouter()

#!GET ALL
@purchase_order_router.get("/admin/obtenersOCS", status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener todas las ordenes de compra')
async def get_all(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    # Obtener todas las ordenes de compra
    purchase_orders = db.query(PurchaseOrderModel).all()

    # Crear Json de respuesta
    response = []

    for purchase_order in purchase_orders:
        # Obtener el proveedor de la orden de compra
        supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == purchase_order.supplier_id).first()

        # Obtener el trabajador de la orden de compra
        worker = db.query(WorkerModel).filter(WorkerModel.id == purchase_order.worker_id).first()
        user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

        # Obtener los detalles de la orden de compra
        details_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.purchase_order_id == purchase_order.id).all()

        # Crear Json de detalles de la orden de compra
        details_purchase_order_json = []

        for detail_purchase_order in details_purchase_order:
            # Obtener el producto del detalle de la orden de compra
            product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
            # Obtener marca del producto
            brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
            # Obtener modelo del producto
            model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

            # Crear Json de detalle de la orden de compra
            detail_purchase_order_json = {
                'id': detail_purchase_order.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'path_image': product.path_image,
                    'brand': brand,
                    'model': model,
                },
                'quantity': detail_purchase_order.quantity
            }

            # Agregar detalle de la orden de compra al Json de detalles de la orden de compra
            details_purchase_order_json.append(detail_purchase_order_json)

        # Crear Json de orden de compra
        purchase_order_json = {
            'id': purchase_order.id,
            'supplier': supplier,
            'worker': {
                'id': worker.id,
                'user': {
                    'num_doc': user_worker.num_doc,
                    'username': user_worker.username,
                    'full_name': user_worker.full_name,
                    'email': user_worker.email,
                    'is_active': user_worker.is_active
                }
            },
            'created_at': purchase_order.created_at,
            'details_purchase_order': details_purchase_order_json
        }

        # Agregar orden de compra al Json de respuesta
        response.append(purchase_order_json)

    return response

#!GET ONE
@purchase_order_router.get("/admin/obtenerOC/{purchase_order_id}", status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener una orden de compra')
async def get_one(purchase_order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    # Obtener orden de compra
    purchase_order = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == purchase_order_id).first()

    # Obtener el proveedor de la orden de compra
    supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == purchase_order.supplier_id).first()

    # Obtener el trabajador de la orden de compra
    worker = db.query(WorkerModel).filter(WorkerModel.id == purchase_order.worker_id).first()
    user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

    # Obtener los detalles de la orden de compra
    details_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.purchase_order_id == purchase_order.id).all()

    # Crear Json de detalles de la orden de compra
    details_purchase_order_json = []

    for detail_purchase_order in details_purchase_order:
        # Obtener el producto del detalle de la orden de compra
        product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
        # Obtener marca del producto
        brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
        # Obtener modelo del producto
        model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

        # Crear Json de detalle de la orden de compra
        detail_purchase_order_json = {
            'id': detail_purchase_order.id,
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'path_image': product.path_image,
                'brand': brand,
                'model': model,
            },
            'quantity': detail_purchase_order.quantity
        }

        # Agregar detalle de la orden de compra al Json de detalles de la orden de compra
        details_purchase_order_json.append(detail_purchase_order_json)

    # Crear Json de orden de compra
    purchase_order_json = {
        'id': purchase_order.id,
        'supplier': supplier,
        'worker': {
            'id': worker.id,
            'user': {
                'num_doc': user_worker.num_doc,
                'username': user_worker.username,
                'full_name': user_worker.full_name,
                'email': user_worker.email,
                'is_active': user_worker.is_active
            }
        },
        'created_at': purchase_order.created_at,
        'details_purchase_order': details_purchase_order_json
    }

    return purchase_order_json

#! GET BY WORKER
@purchase_order_router.get("/admin/obtenerOCTrabajador/{worker_id}", status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener ordenes de compra por trabajador')
async def get_one(worker_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    # Obtener ordenes de compra
    purchase_orders = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.worker_id == worker_id).all()

    # Crear Json de respuesta
    response = []

    for purchase_order in purchase_orders:
        # Obtener el proveedor de la orden de compra
        supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == purchase_order.supplier_id).first()

        # Obtener el trabajador de la orden de compra
        worker = db.query(WorkerModel).filter(WorkerModel.id == purchase_order.worker_id).first()
        user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

        # Obtener los detalles de la orden de compra
        details_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.purchase_order_id == purchase_order.id).all()

        # Crear Json de detalles de la orden de compra
        details_purchase_order_json = []

        for detail_purchase_order in details_purchase_order:
            # Obtener el producto del detalle de la orden de compra
            product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
            # Obtener marca del producto
            brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
            # Obtener modelo del producto
            model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

            # Crear Json de detalle de la orden de compra
            detail_purchase_order_json = {
                'id': detail_purchase_order.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'path_image': product.path_image,
                    'brand': brand,
                    'model': model,
                },
                'quantity': detail_purchase_order.quantity
            }

            # Agregar detalle de la orden de compra al Json de detalles de la orden de compra
            details_purchase_order_json.append(detail_purchase_order_json)

        # Crear Json de orden de compra
        purchase_order_json = {
            'id': purchase_order.id,
            'supplier': supplier,
            'worker': {
                'id': worker.id,
                'user': {
                    'num_doc': user_worker.num_doc,
                    'username': user_worker.username,
                    'full_name': user_worker.full_name,
                    'email': user_worker.email,
                    'is_active': user_worker.is_active
                }
            },
            'created_at': purchase_order.created_at,
            'details_purchase_order': details_purchase_order_json
        }

        # Agregar orden
        response.append(purchase_order_json)

    return response

#! GET BY SUPPLIER
@purchase_order_router.get("/admin/obtenerOCProveedor/{supplier_id}", status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener ordenes de compra por proveedor')
async def get_one(supplier_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    # Obtener ordenes de compra
    purchase_orders = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.supplier_id == supplier_id).all()

    # Crear Json de respuesta
    response = []

    for purchase_order in purchase_orders:
        # Obtener el proveedor de la orden de compra
        supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == purchase_order.supplier_id).first()

        # Obtener el trabajador de la orden de compra
        worker = db.query(WorkerModel).filter(WorkerModel.id == purchase_order.worker_id).first()
        user_worker = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()

        # Obtener los detalles de la orden de compra
        details_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.purchase_order_id == purchase_order.id).all()

        # Crear Json de detalles de la orden de compra
        details_purchase_order_json = []

        for detail_purchase_order in details_purchase_order:
            # Obtener el producto del detalle de la orden de compra
            product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
            # Obtener marca del producto
            brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
            # Obtener modelo del producto
            model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

            # Crear Json de detalle de la orden de compra
            detail_purchase_order_json = {
                'id': detail_purchase_order.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'path_image': product.path_image,
                    'brand': brand,
                    'model': model,
                },
                'quantity': detail_purchase_order.quantity
            }

            # Agregar detalle de la orden de compra al Json de detalles de la orden de compra
            details_purchase_order_json.append(detail_purchase_order_json)

        # Crear Json de orden de compra
        purchase_order_json = {
            'id': purchase_order.id,
            'supplier': supplier,
            'worker': {
                'id': worker.id,
                'user': {
                    'num_doc': user_worker.num_doc,
                    'username': user_worker.username,
                    'full_name': user_worker.full_name,
                    'email': user_worker.email,
                    'is_active': user_worker.is_active
                }
            },
            'created_at': purchase_order.created_at,
            'details_purchase_order': details_purchase_order_json
        }

        # Agregar orden
        response.append(purchase_order_json)

    return response

#! POST - CREATE
@purchase_order_router.post("/admin/crearOC", status_code=status.HTTP_201_CREATED, name='TRABAJADOR - Crear orden de compra')
async def create(purchase_order: PurchaseOrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')

    # Obtener el proveedor de la orden de compra
    supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == purchase_order.supplier_id).first()

    # Obtener el trabajador de la orden de compra
    worker = db.query(WorkerModel).filter(WorkerModel.id == purchase_order.worker_id).first()

    # Crear orden de compra
    purchase_order = PurchaseOrderModel(
        supplier_id = purchase_order.supplier_id,
        worker_id = purchase_order.worker_id,
        created_at = datetime.now()
    )

    # Agregar orden de compra a la base de datos
    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)

    # Crear Json de respuesta
    response = {
        'id': purchase_order.id,
        'supplier': supplier,
        'worker': worker,
        'created_at': purchase_order.created_at
    }

    return response

#! CREATE DETAIL PURCHASE ORDER
@purchase_order_router.post("/admin/crearDetalleOC", status_code=status.HTTP_201_CREATED, name='TRABAJADOR - Crear detalle de orden de compra')
async def create_detail_purchase_order(detail_purchase_order: DetailPurchaseOrderPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    
    # Obtener la orden de compra
    purchase_order = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == detail_purchase_order.purchase_order_id).first()

    if purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No existe la orden de compra')

    # Obtener el producto del detalle de la orden de compra
    product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
    # Obtener marca del producto
    brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
    # Obtener modelo del producto
    model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

    # Crear detalle de orden de compra
    detail_purchase_order = DetailPurchaseOrderModel(
        purchase_order_id = detail_purchase_order.purchase_order_id,
        product_id = detail_purchase_order.product_id,
        quantity = detail_purchase_order.quantity
    )

    # Agregar detalle de orden de compra a la base de datos
    db.add(detail_purchase_order)
    db.commit()
    db.refresh(detail_purchase_order)

    # Crear Json de respuesta
    response = {
        'id': detail_purchase_order.id,
        'product': {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'path_image': product.path_image,
            'brand': brand,
            'model': model,
        },
        'quantity': detail_purchase_order.quantity
    }

    return response

#! PUT - UPDATE DETAIL PURCHASE ORDER
@purchase_order_router.put("/admin/actualizarDetalleOC/{detail_purchase_order_id}", status_code=status.HTTP_200_OK, name='TRABAJADOR - Actualizar detalle de orden de compra')
async def update_detail_purchase_order(detail_purchase_order_id: int, detail_purchase_order: DetailPurchaseOrderPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    
    # Obtener el detalle de la orden de compra
    detail_purchase_order_db = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.id == detail_purchase_order_id).first()

    # Obtener el producto del detalle de la orden de compra
    product = db.query(ProductModel).filter(ProductModel.id == detail_purchase_order.product_id).first()
    # Obtener marca del producto
    brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
    # Obtener modelo del producto
    model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()

    if detail_purchase_order_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No existe el detalle de la orden de compra')

    # Actualizar detalle de orden de compra
    detail_purchase_order_db.quantity = detail_purchase_order.quantity

    # Actualizar detalle de orden de compra en la base de datos
    db.commit()
    db.refresh(detail_purchase_order_db)

    # Crear Json de respuesta
    response = {
        'id': detail_purchase_order_db.id,
        'product': {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'path_image': product.path_image,
            'brand': brand,
            'model': model,
        },
        'quantity': detail_purchase_order_db.quantity
    }

    return response

#! DELETE - DELETE DETAIL PURCHASE ORDER
@purchase_order_router.delete("/admin/eliminarDetalleOC/{detail_purchase_order_id}", status_code=status.HTTP_200_OK, name='TRABAJADOR - Eliminar detalle de orden de compra')
async def delete_detail_purchase_order(detail_purchase_order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    
    # Obtener el detalle de la orden de compra
    detail_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.id == detail_purchase_order_id).first()

    if detail_purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No existe el detalle de la orden de compra')

    # Eliminar detalle de orden de compra de la base de datos
    db.delete(detail_purchase_order)
    db.commit()

    return {'detail': 'Se eliminó correctamente el detalle de la orden de compra'}

#! DELETE - ELIMINAR ORDEN DE COMPRA
@purchase_order_router.delete("/admin/eliminarOC/{purchase_order_id}", status_code=status.HTTP_200_OK, name='TRABAJADOR - Eliminar orden de compra')
async def delete_purchase_order(purchase_order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    
    # Obtener la orden de compra
    purchase_order = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == purchase_order_id).first()

    if purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No existe la orden de compra')

    # Obtener detalles de la orden de compra
    details_purchase_order = db.query(DetailPurchaseOrderModel).filter(DetailPurchaseOrderModel.purchase_order_id == purchase_order_id).all()

    # Eliminar detalles de la orden de compra de la base de datos
    for detail_purchase_order in details_purchase_order:
        db.delete(detail_purchase_order)
        db.commit()

    # Eliminar orden de compra de la base de datos
    db.delete(purchase_order)
    db.commit()

    return {'detail': 'Se eliminó correctamente la orden de compra'}

