from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.model import Model as ModelModel
from app.schemas.model import Model

model_pu = APIRouter()

@model_pu.get('/listadoModelos', response_model=List[Model])
async def listar_modelos(db: Session = Depends(get_db)):
    models = db.query(ModelModel).all()
    return models

@model_pu.get('/obtenerModelo/{id_model}')
async def obtener_modelo(id_model: int, db: Session = Depends(get_db)):
    model = db.query(ModelModel).filter(ModelModel.id_model == id_model).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe el modelo')
    return model