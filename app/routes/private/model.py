from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.model import Model as ModelModel
from app.schemas.model import Model, ModelPost, ModelPut

model_pr = APIRouter()

@model_pr.post('/crearModelo', response_model=Model)
async def crear_modelo(model: ModelPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        new_model = ModelModel(name=model.name, description=model.description, brand_id=model.brand_id)
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        return new_model
    
@model_pr.put('/actualizarModelo/{id_model}', response_model=Model)
async def actualizar_modelo(id_model: int, model: ModelPut, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        model_db = db.query(ModelModel).filter(ModelModel.id == id_model).first()
        if not model_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el modelo')
        model_db.description = model.description
        db.commit()
        db.refresh(model_db)
        return model_db
    
@model_pr.delete('/eliminarModelo/{id_model}')
async def eliminar_modelo(id_model: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        model_db = db.query(ModelModel).filter(ModelModel.id == id_model).first()
        if not model_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el modelo')
        db.delete(model_db)
        db.commit()
        return {'message': 'Se eliminó el modelo'}


