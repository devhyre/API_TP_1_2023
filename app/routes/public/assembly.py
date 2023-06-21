from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.assembly import Assembly as AssemblyModel
from app.models.product import Product as ProductModel

assemblies_pu = APIRouter()

#!OBTENER ASSEMBLLIES POR EL ID DEL MAJOR PRODUCT
#CASE
#PLACA
#PROCESADOR
#RAM
#ALMACENAMIENTO
#CPU_COOLER(*)
#GPU(*)
#FAN(*)
#FUENTE(*)
#MONITOR(*)
#MOUSE(*)
#TECLADO(*)
#CAMARA(*)
#AUDIFONOS(*)
#MICROFONO(*)
#PARLANTES(*)

@assemblies_pu.get('/obtenerAssemblies/{id}', status_code=status.HTTP_200_OK)
async def obtener_assemblies(case_id: int = None, placa_id: int = None, procesador_id: int = None, ram_id: int=None, almacenamiento: int=None,
                             gpu_id: int = None, fan_id: int = None, fuente_id: int = None, monitor_id: int = None, mouse_id: int=None, teclado_id:int=None,
                             camara_id: int = None, audifono_id: int = None, microfono_id: int = None, parlante_id: int = None, db: Session = Depends(get_db)):
    #!OBTENER TODAS LAS RECOMENDACIONES DE COMPATIBILIDAD DE PRODUCTOS
    recomendaciones = db.query(AssemblyModel).all()
    #!OBTENER TODOS LOS PRODUCTOS
    productos = db.query(ProductModel).all()
    
    #SOLO MOSTRAR LOS CASES
    FILTRO_SOLO_CASE = filter(lambda product: product.category_id == 7, productos)
    productos = list(FILTRO_SOLO_CASE)
    
    if
    
    return productos