from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.model import Model as ModelModel
from app.models.brand import Brand as BrandModel
from app.schemas.model import Model, ModelPost, ModelPut
from app.models.product import Product as ProductModel

model_pr = APIRouter()

@model_pr.post('/admin/crearModelo', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR - Crear modelo')
async def crear_modelo(model: ModelPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        brand_exist = db.query(BrandModel).filter(BrandModel.id == model.brand_id).first()
        if not brand_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
        new_model = ModelModel(name=model.name, description=model.description, brand_id=model.brand_id)
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        return {'message': 'Modelo creado satisfactoriamente', 'data': new_model}
    
@model_pr.put('/admin/actualizarModelo/{id_model}', status_code=status.HTTP_202_ACCEPTED , name='ADMINISTRADOR - Actualizar modelo')
async def actualizar_modelo(id_model: int, model: ModelPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        model_db = db.query(ModelModel).filter(ModelModel.id == id_model).first()
        if not model_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el modelo')
        db.query(ModelModel).filter(ModelModel.id == id_model).update({ModelModel.name: model.name, ModelModel.description: model.description})
        model_updated = db.query(ModelModel).filter(ModelModel.id == id_model).first()
        return {'message': 'Modelo actualizado satisfactoriamente', 'data': model_updated}
    
@model_pr.delete('/admin/eliminarModelo/{id_model}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Eliminar modelo')
async def eliminar_modelo(id_model: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        model_db = db.query(ModelModel).filter(ModelModel.id == id_model).first()
        if not model_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el modelo')
        products = db.query(ProductModel).filter(ProductModel.model_id == id_model).all()
        if products:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='No se puede eliminar el modelo porque tiene productos asociados')
        db.delete(model_db)
        return {'message': 'Modelo eliminado satisfactoriamente'}