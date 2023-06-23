from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.combo import Combo as ComboModel
from app.models.detail_combo import DetailCombo as DetailComboModel
from app.models.product import Product as ProductModel
from app.schemas.product import Product as ProductSchema
from app.schemas.detail_combo import DetailCombo as DetailComboSchema
from datetime import datetime

combo_pu = APIRouter()

#!COMBO
#GET ALL
@combo_pu.get('/combos')
async def get_combos(db: Session = Depends(get_db)):
    Data = {
        'product_id': [],
        'name': [],
        'description': [],
        'path_image': [],
        'quantity': [],
        'discount': [],
        'price': [],
        'warranty': [],
        'category_id': [],
        'brand_id': [],
        'model_id': [],
        'status_id': [],
        'ranking': [],
    }
    #Obtener todos los combos y sus productos asociados luego agregarlos a Data
    combos = db.query(ComboModel).all()
    for combo in combos:
        product = db.query(ProductModel).filter(ProductModel.id == combo.product_id).first()
        Data['product_id'].append(product.id)
        Data['name'].append(product.name)
        Data['description'].append(product.description)
        Data['path_image'].append(product.path_image)
        Data['quantity'].append(product.quantity)
        Data['discount'].append(product.discount)
        Data['price'].append(product.price)
        Data['warranty'].append(product.warranty)
        Data['category_id'].append(product.category_id)
        Data['brand_id'].append(product.brand_id)
        Data['model_id'].append(product.model_id)
        Data['status_id'].append(product.status_id)
        Data['ranking'].append(product.ranking)
    return Data


#get id
@combo_pu.get('/combo/{combo_id}')
async def get_combo(combo_id: str, db: Session = Depends(get_db)):
    Data = {
        'product_id': [],
        'name': [],
        'description': [],
        'path_image': [],
        'quantity': [],
        'discount': [],
        'price': [],
        'warranty': [],
        'category_id': [],
        'brand_id': [],
        'model_id': [],
        'status_id': [],
        'ranking': [],
    }
    #Obtener todos los combos y sus productos asociados luego agregarlos a Data
    combo = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    product = db.query(ProductModel).filter(ProductModel.id == combo.product_id).first()
    Data['product_id'].append(product.id)
    Data['name'].append(product.name)
    Data['description'].append(product.description)
    Data['path_image'].append(product.path_image)
    Data['quantity'].append(product.quantity)
    Data['discount'].append(product.discount)
    Data['price'].append(product.price)
    Data['warranty'].append(product.warranty)
    Data['category_id'].append(product.category_id)
    Data['brand_id'].append(product.brand_id)
    Data['model_id'].append(product.model_id)
    Data['status_id'].append(product.status_id)
    Data['ranking'].append(product.ranking)
    return Data


#!COMBO DETAIL
#get combo detail id all
@combo_pu.get('/combo_detail/{combo_id}')
async def get_combo_detail(combo_id: str, db: Session = Depends(get_db)):
    Data = {
        'product_id': [],
        'name': [],
        'description': [],
        'path_image': [],
        'quantity': [],
        'discount': [],
        'price': [],
        'warranty': [],
        'category_id': [],
        'brand_id': [],
        'model_id': [],
        'status_id': [],
        'ranking': [],
    }
    #Obtener todos los combos y sus productos asociados luego agregarlos a Data
    combo_detail = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_id).all()
    for detail in combo_detail:
        product = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
        Data['product_id'].append(product.id)
        Data['name'].append(product.name)
        Data['description'].append(product.description)
        Data['path_image'].append(product.path_image)
        Data['quantity'].append(product.quantity)
        Data['discount'].append(product.discount)
        Data['price'].append(product.price)
        Data['warranty'].append(product.warranty)
        Data['category_id'].append(product.category_id)
        Data['brand_id'].append(product.brand_id)
        Data['model_id'].append(product.model_id)
        Data['status_id'].append(product.status_id)
        Data['ranking'].append(product.ranking)
    return Data