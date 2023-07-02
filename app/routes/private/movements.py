from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.movement import Movement as MovementModel
from app.models.sn import SerialNumber as SerialNumberModel
from app.models.user import User as UserModel
from app.models.product import Product as ProductModel
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.purchase_order import PurchaseOrder as PurchaseOrderModel

movement_router = APIRouter()

#! Obtener todos los movimientos
@movement_router.get("/admin/movements", status_code=status.HTTP_200_OK, name="ADMINISTRADOR|TRABAJADOR - Obtener todos los movimientos")
async def get_all_movements(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    movements = db.query(MovementModel).all()
    # Obtener el tipo de movimiento
    types_movement = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 10).all()
    types_movement = [{'id': type_movement.id_table, 'description': type_movement.description} for type_movement in types_movement]

    response = []

    for movement in movements:
        # Obtener la serie
        sn = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == movement.sn_id).first()
        # Obtener el producto
        product = db.query(ProductModel).filter(ProductModel.id == sn.product_id).first()
        # Obtener la marca
        brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
        # Obtener el modelo
        model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
        # Obtener el usuario
        user = db.query(UserModel).filter(UserModel.num_doc == movement.user_id).first()
        # Obtener el tipo de movimiento
        type_movement = [type_movement for type_movement in types_movement if type_movement['id'] == movement.type_id]
        # Obtener la orden de compra
        oc = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == sn.oc_id).first()

        movement_json = {
            'id': movement.id,
            'sn': {
                'serial_number': movement.sn_id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'brand': {
                        'id': brand.id,
                        'name': brand.name
                    },
                    'model': {
                        'id': model.id,
                        'name': model.name
                    }
                },
                'oc': oc,
            },
            'user': {
                'num_doc': user.num_doc,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'is_active': user.is_active
            },
            'created_at': movement.created_at,
            'type': type_movement
        }
        response.append(movement_json)

    return response

#! Obtener movimiento por id
@movement_router.get("/admin/movements/{movement_id}", status_code=status.HTTP_200_OK, name="ADMINISTRADOR|TRABAJADOR - Obtener movimiento por id")
async def get_movement_by_id(movement_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    movement = db.query(MovementModel).filter(MovementModel.id == movement_id).first()
    # Obtener el tipo de movimiento
    types_movement = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 10).all()
    types_movement = [{'id': type_movement.id_table, 'description': type_movement.description} for type_movement in types_movement]

    # Obtener la serie
    sn = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == movement.sn_id).first()
    # Obtener el producto
    product = db.query(ProductModel).filter(ProductModel.id == sn.product_id).first()
    # Obtener la marca
    brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
    # Obtener el modelo
    model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
    # Obtener el usuario
    user = db.query(UserModel).filter(UserModel.num_doc == movement.user_id).first()
    # Obtener el tipo de movimiento
    type_movement = [type_movement for type_movement in types_movement if type_movement['id'] == movement.type_id]
    # Obtener la orden de compra
    oc = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == sn.oc_id).first()

    movement_json = {
        'id': movement.id,
        'sn': {
            'serial_number': movement.sn_id,
            'product': {
                'id': product.id,
                'name': product.name,
                'brand': {
                    'id': brand.id,
                    'name': brand.name
                },
                'model': {
                    'id': model.id,
                    'name': model.name
                }
            },
            'oc': oc,
        },
        'user': {
            'num_doc': user.num_doc,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'is_active': user.is_active
        },
        'created_at': movement.created_at,
        'type': type_movement
    }

    return movement_json

#! Obtener movimientos por serie
@movement_router.get("/admin/movements/sn/{sn_id}", status_code=status.HTTP_200_OK, name="ADMINISTRADOR|TRABAJADOR - Obtener movimientos por serie")
async def get_movements_by_sn(sn_id: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    movements = db.query(MovementModel).filter(MovementModel.sn_id == sn_id).all()
    # Obtener el tipo de movimiento
    types_movement = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 10).all()
    types_movement = [{'id': type_movement.id_table, 'description': type_movement.description} for type_movement in types_movement]

    response = []

    for movement in movements:
        # Obtener la serie
        sn = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == movement.sn_id).first()
        # Obtener el producto
        product = db.query(ProductModel).filter(ProductModel.id == sn.product_id).first()
        # Obtener la marca
        brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
        # Obtener el modelo
        model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
        # Obtener el usuario
        user = db.query(UserModel).filter(UserModel.num_doc == movement.user_id).first()
        # Obtener el tipo de movimiento
        type_movement = [type_movement for type_movement in types_movement if type_movement['id'] == movement.type_id]
        # Obtener la orden de compra
        oc = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == sn.oc_id).first()

        movement_json = {
            'id': movement.id,
            'sn': {
                'serial_number': movement.sn_id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'brand': {
                        'id': brand.id,
                        'name': brand.name
                    },
                    'model': {
                        'id': model.id,
                        'name': model.name
                    }
                },
                'oc': oc,
            },
            'user': {
                'num_doc': user.num_doc,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'is_active': user.is_active
            },
            'created_at': movement.created_at,
            'type': type_movement
        }
        response.append(movement_json)

    return response

#! Obtener movimientos por usuario
@movement_router.get("/admin/movements/user/{user_id}", status_code=status.HTTP_200_OK, name="ADMINISTRADOR|TRABAJADOR - Obtener movimientos por usuario")
async def get_movements_by_user(user_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No tiene permisos para realizar esta acción')
    movements = db.query(MovementModel).filter(MovementModel.user_id == user_id).all()
    # Obtener el tipo de movimiento
    types_movement = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 10).all()
    types_movement = [{'id': type_movement.id_table, 'description': type_movement.description} for type_movement in types_movement]

    response = []

    for movement in movements:
        # Obtener la serie
        sn = db.query(SerialNumberModel).filter(SerialNumberModel.sn_id == movement.sn_id).first()
        # Obtener el producto
        product = db.query(ProductModel).filter(ProductModel.id == sn.product_id).first()
        # Obtener la marca
        brand = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
        # Obtener el modelo
        model = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
        # Obtener el usuario
        user = db.query(UserModel).filter(UserModel.num_doc == movement.user_id).first()
        # Obtener el tipo de movimiento
        type_movement = [type_movement for type_movement in types_movement if type_movement['id'] == movement.type_id]
        # Obtener la orden de compra
        oc = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == sn.oc_id).first()

        movement_json = {
            'id': movement.id,
            'sn': {
                'serial_number': movement.sn_id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'brand': {
                        'id': brand.id,
                        'name': brand.name
                    },
                    'model': {
                        'id': model.id,
                        'name': model.name
                    }
                },
                'oc': oc,
            },
            'user': {
                'num_doc': user.num_doc,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'is_active': user.is_active
            },
            'created_at': movement.created_at,
            'type': type_movement
        }
        response.append(movement_json)

    return response