from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.combo import Combo as ComboModel
from app.models.product import Product as ProductModel
from app.schemas.combo import ComboPost
from datetime import datetime

combo_pr = APIRouter()

#!Combo
@combo_pr.post('/admin/crearCombo', status_code=status.HTTP_201_CREATED, name='TRABAJADOR - Crear combo')
async def create_combo(combo: ComboPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    #Verificar si los productos existen
    lista_productos = [combo.case_id, combo.motherboard_id, combo.procesador_id, combo.ram_id, combo.almacenamiento_id, combo.cooler_id, combo.gpu_id, combo.fan_id, combo.fuente_id]
    for product_id in lista_productos:
        if product_id is None:
            continue
        product_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto no encontrado')
    #Verificar si el id del producto no es nulo, entonces la cantidad debe ser mayor a 0
    lista_cantidades = [combo.quantity_case, combo.quantity_motherboard, combo.quantity_procesador, combo.quantity_ram, combo.quantity_almacenamiento, combo.quantity_cooler, combo.quantity_gpu, combo.quantity_fan, combo.quantity_fuente]
    for i in range(len(lista_productos)):
        if lista_productos[i] is None:
            continue
        if lista_cantidades[i] is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La cantidad de productos debe ser mayor a 0')
    #Crear ID de combo que sera compuesto por COM+CATEGORIA+ID
    number_random = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
    combo_id = 'COM' + number_random
    #Crear combo
    combo_db = ComboModel(
        id = combo_id,
        name = combo.name,
        description = combo.description,
        path_image = combo.path_image,
        case_id = combo.case_id,
        case_quantity = combo.quantity_case,
        motherboard_id = combo.motherboard_id,
        motherboard_quantity = combo.quantity_motherboard,
        procesador_id = combo.procesador_id,
        processor_quantity = combo.quantity_procesador,
        ram_id = combo.ram_id,
        ram_quantity = combo.quantity_ram,
        almacenamiento_id = combo.almacenamiento_id,
        almacenamiento_quantity = combo.quantity_almacenamiento,
        cooler_id = combo.cooler_id,
        cooler_quantity = combo.quantity_cooler,
        gpu_id = combo.gpu_id,
        gpu_quantity = combo.quantity_gpu,
        fan_id = combo.fan_id,
        fan_quantity = combo.quantity_fan,
        fuente_id = combo.fuente_id,
        fuente_quantity = combo.quantity_fuente,
        created_at = datetime.now(),
        worker_id = user[user_type]['id']
    )
    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return {'detail': 'Combo creado, su ID es: ' + combo_id}

@combo_pr.delete('/admin/eliminarCombo/{combo_id}', status_code=status.HTTP_204_NO_CONTENT, name='TRABAJADOR - Eliminar combo')
async def delete_combo(combo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'worker':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

    # Verificar si el combo existe
    combo_db = db.query(ComboModel).filter(ComboModel.id == combo_id).first()
    if not combo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Combo no encontrado')
    
    # Eliminar combo
    db.delete(combo_db)
    db.commit()
    return {'detail': 'Combo eliminado'}