from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db

from app.models.role_privileges import RolePrivilege as RolePrivilegeModel
from app.schemas.role_privileges import RolePrivilege, RolePrivilegePost, RolePrivilegePut

from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

role_privileges = APIRouter()

@role_privileges.get('/listarPrivilegiosRol', status_code=status.HTTP_200_OK)
async def listar_privilegios_rol(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role_privileges = db.query(RolePrivilegeModel).all()
        return [role_privileges for role_privilege in role_privileges]
    
@role_privileges.get('/obtenerPrivilegiosRol/{id_role}', status_code=status.HTTP_200_OK)
async def obtener_privilegios_rol(id_role: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        role_privilege = db.query(RolePrivilegeModel).filter(RolePrivilegeModel.id_role == id_role).first()
        if role_privilege:
            return role_privilege
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El rol no existe')
    
@role_privileges.post('/crearPrivilegioRol', status_code=status.HTTP_201_CREATED)
async def crear_privilegio_rol(role_privilege: RolePrivilegePost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        new_role_privilege = RolePrivilegeModel(**role_privilege.dict())
        db.add(new_role_privilege)
        db.commit()
        db.refresh(new_role_privilege)
        return new_role_privilege
    
@role_privileges.put('/actualizarPrivilegioRol/{id_role}', status_code=status.HTTP_200_OK)
async def actualizar_privilegio_rol(id_role: int, role_privilege: RolePrivilegePut, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    if id_role == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se puede modificar el rol de administrador')
    else:
        role_privilege_db = db.query(RolePrivilegeModel).filter(RolePrivilegeModel.id_role == id_role).first()
        if role_privilege_db:
            role_privilege_db.module_1 = role_privilege.module_1
            role_privilege_db.module_2 = role_privilege.module_2
            role_privilege_db.module_3 = role_privilege.module_3
            role_privilege_db.module_4 = role_privilege.module_4
            role_privilege_db.module_5 = role_privilege.module_5
            role_privilege_db.module_6 = role_privilege.module_6
            role_privilege_db.module_7 = role_privilege.module_7
            role_privilege_db.module_8 = role_privilege.module_8
            role_privilege_db.module_9 = role_privilege.module_9
            role_privilege_db.module_10 = role_privilege.module_10
            role_privilege_db.module_11 = role_privilege.module_11
            role_privilege_db.module_12 = role_privilege.module_12
            role_privilege_db.module_13 = role_privilege.module_13
            role_privilege_db.module_14 = role_privilege.module_14
            role_privilege_db.module_15 = role_privilege.module_15
            role_privilege_db.module_16 = role_privilege.module_16
            role_privilege_db.module_17 = role_privilege.module_17
            role_privilege_db.module_18 = role_privilege.module_18
            role_privilege_db.module_19 = role_privilege.module_19
            role_privilege_db.module_20 = role_privilege.module_20
            db.commit()
            db.refresh(role_privilege_db)
            return role_privilege_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El rol no existe')