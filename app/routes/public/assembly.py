from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.assembly import Assembly as AssemblyModel

assemblies_pu = APIRouter()

#!OBTENER ASSEMBLLIES POR EL ID DEL MAJOR PRODUCT
@assemblies_pu.get('/obtenerAssemblies/{id}')
async def obtener_assemblies(id: int, db: Session = Depends(get_db)):
    assemblies = db.query(AssemblyModel).filter(AssemblyModel.major_product_id == id).all()
    return assemblies
    
