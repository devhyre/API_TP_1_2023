from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.brand import Brand as BrandModel

brand_pu = APIRouter()

@brand_pu.get('/listadoMarcas', status_code=status.HTTP_200_OK, name='Listado de marcas')
async def listar_marcas(db: Session = Depends(get_db)):
    brands = db.query(BrandModel).all()
    return [brand for brand in brands]

@brand_pu.get('/obtenerMarca/{id_brand}', status_code=status.HTTP_200_OK, name='Obtener marca')
async def obtener_marca(id_brand: int, db: Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.id == id_brand).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
    return brand