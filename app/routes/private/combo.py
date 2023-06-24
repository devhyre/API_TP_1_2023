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
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel

combo_pr = APIRouter()

#!Combo
@combo_pr.post('/combo')
async def create_combo(product: ProductSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    product_db = db.query(ProductModel).filter(ProductModel.id == product.name).first()
    #Si el producto existe
    if product_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El producto ya existe')
    #Si la marca no existe
    brand_db = db.query(BrandModel).filter(BrandModel.id == product.brand_id).first()
    if not brand_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='La marca no existe')
    #Si el modelo no existe
    model_db = db.query(ModelModel).filter(ModelModel.id == product.model_id).first()
    if not model_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El modelo no existe')
    #Si el producto no existe
    product_db = ProductModel(
            name = product.name,
            description = product.description,
            path_image = product.path_image,
            quantity = 0,
            price = product.price,
            discount = product.discount,
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
    #Crear ID de combo que sera compuesto por COM+CATEGORIA+ID
    combo_id = 'COM' + str(product.category_id) + str(product_db.id)
    #Crear combo
    combo_db = ComboModel(
        id = combo_id,
        product_id = product_db.id,
        created_at = datetime.now(),
        worker_id = user[user_type]['id']
    )
    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return {'detail': 'Combo creado, su ID es: ' + combo_id + ' y su ID de producto es: ' + str(product_db.id)}

@combo_pr.delete('/combo/{product_id}')
async def delete_combo(product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

    # Verificar si el producto existe
    product_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no existe')
    
    # Verificar si el producto es un combo
    combo_db = db.query(ComboModel).filter(ComboModel.product_id == product_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no es un combo')
    
    # Verificar si el producto tiene detalles
    detail_combo_db = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_db.id).first()
    if detail_combo_db:
        # Eliminar los detalles del combo
        db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_db.id).delete()
        db.commit()

    # Eliminar el combo
    db.query(ComboModel).filter(ComboModel.product_id == product_id).delete()
    db.commit()

    # Eliminar el producto
    db.query(ProductModel).filter(ProductModel.id == product_id).delete()
    db.commit()

    return {'detail': 'Combo eliminado'}

#!COMBO DETAIL
@combo_pr.post('/combo/{combo_id}/detail')
async def create_combo_detail(combo_id: int, detail_combo: DetailComboSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

    # Verificar si el combo existe
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El combo no existe')
    
    # Verificar si el producto existe
    product_db = db.query(ProductModel).filter(ProductModel.id == detail_combo.product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no existe')
    
    # Verificar si el producto es un combo
    combo_db = db.query(ComboModel).filter(ComboModel.product_id == detail_combo.product_id).first()
    if combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto es un combo')
    
    # Verificar si el producto ya esta en el combo
    detail_combo_db = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_id, DetailComboModel.product_id == detail_combo.product_id).first()
    #Si ya esta en en el combo se actualiza la cantidad
    if detail_combo_db:
        detail_combo_db.quantity += detail_combo.quantity
        db.commit()
        db.refresh(detail_combo_db)
        return detail_combo_db
    #Si no esta en el combo se crea
    detail_combo_db = DetailComboModel(
        product_id = detail_combo.product_id,
        quantity = detail_combo.quantity,
        combo_id = combo_id
    )
    db.add(detail_combo_db)
    db.commit()
    db.refresh(detail_combo_db)
    return detail_combo_db

#PUT
@combo_pr.put('/combo/{combo_id}/detail/{product_id}')
async def update_combo_detail(combo_id: int, product_id: int, detail_combo: DetailComboSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

    # Verificar si el combo existe
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El combo no existe')
    
    # Verificar si el producto existe
    product_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no existe')
    
    # Verificar si el producto es un combo
    combo_db = db.query(ComboModel).filter(ComboModel.product_id == product_id).first()
    if combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto es un combo')
    
    # Verificar si el producto ya esta en el combo
    detail_combo_db = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_id, DetailComboModel.product_id == product_id).first()
    #Si ya esta en en el combo se actualiza la cantidad
    if detail_combo_db:
        detail_combo_db.quantity = detail_combo.quantity
        db.commit()
        db.refresh(detail_combo_db)
        return detail_combo_db
    #Si no esta en el combo se crea
    detail_combo_db = DetailComboModel(
        product_id = product_id,
        quantity = detail_combo.quantity,
        combo_id = combo_id
    )
    db.add(detail_combo_db)
    db.commit()
    db.refresh(detail_combo_db)
    return detail_combo_db

#DELETE
@combo_pr.delete('/combo/{combo_id}/detail/{product_id}')
async def delete_combo_detail(combo_id: int, product_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

    # Verificar si el combo existe
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El combo no existe')
    
    # Verificar si el producto existe
    product_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no existe')
    
    # Verificar si el producto es un combo
    combo_db = db.query(ComboModel).filter(ComboModel.product_id == product_id).first()
    if combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto es un combo')
    
    # Verificar si el producto ya esta en el combo
    detail_combo_db = db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_id, DetailComboModel.product_id == product_id).first()
    #Si ya esta en en el combo se elimina
    if detail_combo_db:
        db.query(DetailComboModel).filter(DetailComboModel.combo_id == combo_id, DetailComboModel.product_id == product_id).delete()
        db.commit()
        return {'detail': 'Detalle eliminado'}
    #Si no esta en el combo se crea
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El producto no esta en el combo')