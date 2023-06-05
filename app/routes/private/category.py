from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

categories_pr = APIRouter()

@categories_pr.post('/registrarCategoria', status_code=status.HTTP_201_CREATED)
async def registrar_categoria(id_table:int, description: str, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
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
        return {'id': category.id_table, 'description': category.description}
    
@categories_pr.put('/actualizarCategoria/{id_table}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_categoria(id_table: int, description: str, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con id {id_table} no existe")
        category.description = description
        db.commit()
        db.refresh(category)
        return {'id': category.id_table, 'description': category.description}
    
@categories_pr.delete('/eliminarCategoria/{id_table}', status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_categoria(id_table: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).filter(TableOfTablesModel.id_table == id_table).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con id {id_table} no existe")
        db.delete(category)
        db.commit()
        return {'message': f"La categoria con id {id_table} ha sido eliminada"}
    