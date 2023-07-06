from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

categories_pr = APIRouter()

@categories_pr.post('/admin/registrarCategoria', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR|TRABAJADOR - Registrar categoria')
async def registrar_categoria(id_table:int, description: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        if category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La categoria con id {id_table} ya existe")
        category = TableOfTablesModel(id=3, id_table=id_table, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return {'message': "La categoria ha sido registrada", 'data': category}
    
@categories_pr.put('/admin/actualizarCategoria/{id_table}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR - Actualizar categoria')
async def actualizar_categoria(id_table: int, description: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con id {id_table} no existe")
        db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3, TableOfTablesModel.id_table == id_table).update({TableOfTablesModel.description: description})
        db.commit()
        category_updated = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        return {'message': "La categoria ha sido actualizada", 'data': category_updated}
    
@categories_pr.delete('/admin/eliminarCategoria/{id_table}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Eliminar categoria')
async def eliminar_categoria(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con id {id_table} no existe")
        db.delete(category)
        db.commit()
        return {'message': "La categoria ha sido eliminada"}
    