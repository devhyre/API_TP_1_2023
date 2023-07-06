from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.brand import Brand as BrandModel
from app.schemas.brand import Brand, BrandPost, BrandPut
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.model import Model as ModelModel

brand_pr = APIRouter()

@brand_pr.post('/admin/crearMarca', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR - Crear marca')
async def crear_marca(brand: BrandPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        new_brand = BrandModel(name=brand.name, description=brand.description)
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return {'message': 'Se creó la marca', 'data': new_brand}

@brand_pr.put('/admin/actualizarMarca/{id}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR - Actualizar marca')
async def actualizar_marca(id: int, brand: BrandPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        brand_db = db.query(BrandModel).filter(BrandModel.id == id).first()
        if not brand_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
        db.query(BrandModel).filter(BrandModel.id == id).update({BrandModel.name: brand.name, BrandModel.description: brand.description})
        brand_updated = db.query(BrandModel).filter(BrandModel.id == id).first()
        return {'message': 'Se actualizó la marca',
                'data': brand_updated}

@brand_pr.delete('/admin/eliminarMarca/{id}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Eliminar marca')
async def eliminar_marca(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        brand_db = db.query(BrandModel).filter(BrandModel.id == id).first()
        if not brand_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
        models = db.query(ModelModel).filter(ModelModel.brand_id == id).first()
        if models:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Existen modelos asociados a esta marca')
        db.delete(brand_db)
        db.commit()
        return {'message': 'Se eliminó la marca'}