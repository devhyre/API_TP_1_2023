from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.models.role_privileges import RolePrivilege as RolePrivilegeModel
from app.schemas.role_privileges import RolePrivilegePost, RolePrivilegePut
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

role_privileges = APIRouter()

@role_privileges.get('/admin/listarPrivilegiosRol', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Listar privilegios de roles')
async def listar_privilegios_rol(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener los roles
        roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
        roles =  [{'id': role.id_table, 'description': role.description} for role in roles]
        # Obtener los privilegios
        role_privileges = db.query(RolePrivilegeModel).all()
        # Crear el Json de respuesta
        response = []
        # Recorrer los role_privileges y agregar los roles
        for role_privilege in role_privileges:
            # Obtener el role
            role = next((role for role in roles if role['id'] == role_privilege.role_id), None)
            # Crear el Json del role
            role_json = {
                'role': role,
                'privileges': {
                    'module_1': role_privilege.module_1,
                    'module_2': role_privilege.module_2,
                    'module_3': role_privilege.module_3,
                    'module_4': role_privilege.module_4,
                    'module_5': role_privilege.module_5,
                    'module_6': role_privilege.module_6,
                    'module_7': role_privilege.module_7,
                    'module_8': role_privilege.module_8,
                    'module_9': role_privilege.module_9,
                    'module_10': role_privilege.module_10,
                    'module_11': role_privilege.module_11,
                    'module_12': role_privilege.module_12,
                    'module_13': role_privilege.module_13,
                    'module_14': role_privilege.module_14,
                    'module_15': role_privilege.module_15,
                    'module_16': role_privilege.module_16,
                    'module_17': role_privilege.module_17,
                    'module_18': role_privilege.module_18,
                    'module_19': role_privilege.module_19,
                    'module_20': role_privilege.module_20
                }
            }
            # Agregar el role a la respuesta
            response.append(role_json)
        return response
    
@role_privileges.get('/admin/obtenerPrivilegiosRol/{id_role}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener privilegios de un rol')
async def obtener_privilegios_rol(id_role: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener los roles
        roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
        roles =  [{'id': role.id_table, 'description': role.description} for role in roles]
        # Obtener el role
        role = next((role for role in roles if role['id'] == id_role), None)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {id_role} no existe")
        # Obtener los privilegios
        role_privilege = db.query(RolePrivilegeModel).filter(RolePrivilegeModel.role_id == id_role).first()
        if not role_privilege:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {id_role} no tiene privilegios")
        # Crear el Json de respuesta
        response = {
            'role': {
                'id': role['id'],
                'description': role['description']
            },
            'privileges': {
                'module_1': role_privilege.module_1,
                'module_2': role_privilege.module_2,
                'module_3': role_privilege.module_3,
                'module_4': role_privilege.module_4,
                'module_5': role_privilege.module_5,
                'module_6': role_privilege.module_6,
                'module_7': role_privilege.module_7,
                'module_8': role_privilege.module_8,
                'module_9': role_privilege.module_9,
                'module_10': role_privilege.module_10,
                'module_11': role_privilege.module_11,
                'module_12': role_privilege.module_12,
                'module_13': role_privilege.module_13,
                'module_14': role_privilege.module_14,
                'module_15': role_privilege.module_15,
                'module_16': role_privilege.module_16,
                'module_17': role_privilege.module_17,
                'module_18': role_privilege.module_18,
                'module_19': role_privilege.module_19,
                'module_20': role_privilege.module_20
            }
        }
        return response
        
    
@role_privileges.post('/admin/crearPrivilegioRol', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR - Crear privilegio de un rol')
async def crear_privilegio_rol(role_privilege: RolePrivilegePost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener los roles
        roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
        roles =  [{'id': role.id_table, 'description': role.description} for role in roles]
        # Obtener el role
        role = next((role for role in roles if role['id'] == role_privileges.role_id), None)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con id {role_privileges.role_id} no existe")
        # Si existe el role, crear el privilegio
        new_role_privilege = RolePrivilegeModel(
            role_id = role_privilege.role_id,
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
        db.add(new_role_privilege)
        db.commit()
        db.refresh(new_role_privilege)
        return new_role_privilege
    
@role_privileges.put('/admin/actualizarPrivilegioRol/{id_role}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Actualizar privilegio de un rol')
async def actualizar_privilegio_rol(id_role: int, role_privilege: RolePrivilegePut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    if id_role == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se puede modificar el rol de administrador')
    else:
        role_privilege_db = db.query(RolePrivilegeModel).filter(RolePrivilegeModel.role_id == id_role).first()
        if role_privilege_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El rol no existe')
        else:
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
        
@role_privileges.delete('/admin/eliminarPrivilegioRol/{id_role}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Eliminar privilegio de un rol')
async def eliminar_privilegio_rol(id_role: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    if id_role == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se puede eliminar el rol de administrador')
    else:
        role_privilege_db = db.query(RolePrivilegeModel).filter(RolePrivilegeModel.role_id == id_role).first()
        if role_privilege_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El rol no existe')
        else:
            db.delete(role_privilege_db)
            db.commit()
            return {'detail': 'Se ha eliminado el rol con éxito'}
        

"""
NIVELES DE ACCESO PARA USUARIOS ADMINISTRATIVOS
0: GET
1: GET, POST
2: GET, POST, PUT
3: GET, POST, PUT, DELETE
"""