from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.role_privileges import RolePrivilege as RolePrivilegeModel
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.models.role_privileges import RolePrivilege as RolePrivilegeModel

roles = APIRouter()

@roles.get('/listadoRoles',status_code=status.HTTP_200_OK)
async def listar_roles(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
        return [{'id': role.id_table, 'description': role.description} for role in roles]

@roles.get('/obtenerRol/{id_table}', status_code=status.HTTP_200_OK)
async def obtener_rol(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).filter(TableOfTablesModel.id_table == id_table).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {id_table} no existe")
        return {'id': role.id_table, 'description': role.description}

@roles.post('/registrarRol', status_code=status.HTTP_201_CREATED)
async def registrar_rol(id_table:int, description: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role_exists = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).filter(TableOfTablesModel.id_table == id_table).first()
        if role_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='El rol ya esta registrado')
        role = TableOfTablesModel(id=2, id_table=id_table, description=description)
        new_role_privilege = RolePrivilegeModel(
            role_id = id_table,
            module_1 = False,
            module_2 = False,
            module_3 = False,
            module_4 = False,
            module_5 = False,
            module_6 = False,
            module_7 = False,
            module_8 = False,
            module_9 = False,
            module_10 = False,
            module_11 = False,
            module_12 = False,
            module_13 = False,
            module_14 = False,
            module_15 = False,
            module_16 = False,
            module_17 = False,
            module_18 = False,
            module_19 = False,
            module_20 = False
        )
        db.add(role)
        db.add(new_role_privilege)
        db.commit()
        return {'id': role.id_table, 'description': role.description}

@roles.put('/actualizarRol/{id_table}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_rol(id_table: int, description: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).filter(TableOfTablesModel.id_table == id_table).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {id_table} no existe")
        role.description = description
        db.commit()
        return {'id': role.id_table, 'description': role.description}

@roles.delete('/eliminarRol/{id_table}', status_code=status.HTTP_200_OK)
async def eliminar_rol(id_table: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).filter(TableOfTablesModel.id_table == id_table).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {id_table} no existe")
        db.delete(role)
        db.commit()
        return {'message': f"El rol con id {id_table} ha sido eliminado"}
