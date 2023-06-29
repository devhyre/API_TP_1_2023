from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.token import get_current_active_user
from app.models.worker import Worker as WorkerModel
from app.models.user import User as UserModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

workers = APIRouter()

@workers.get('/admin/obtenerTrabajadores', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Obtener todos los trabajadores')
async def get_workers(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    # Crear el Json de respuesta
    response = []
    # Obtener todos los trabajadores
    workers = db.query(WorkerModel).all()
    # Obtener todos los roles
    roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
    roles = [{'id': role.id_table, 'description': role.description} for role in roles]
    # Recorrer los trabajadores
    for worker in workers:
        # Obtener el usuario del trabajador
        user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
        # Obtener el rol del trabajador
        role = [role for role in roles if role['id'] == worker.role_id][0]
        # Crear el Json del trabajador
        worker_json = {
            'id': worker.id,
            'level': worker.level,
            'user': {
                'numeroDocumento': user.num_doc,
                'nombreCompleto': user.full_name,
                'email': user.email,
                'estado': user.is_active,
                'username': user.username
            },
            'role': {
                'id': role['id'],
                'descripcion': role['description'],
            }
        }
        # Agregar el Json del trabajador al Json de respuesta
        response.append(worker_json)
    return response

@workers.get('/admin/obtenerTrabajador/{dni}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Obtener un trabajador por su N° de documento')
async def get_worker(dni: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    # Obtener el trabajador
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == dni).first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Trabajador no encontrado')
    # Obtener el usuario del trabajador
    user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
    # Obtener todos los roles
    roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
    roles = [{'id': role.id_table, 'description': role.description} for role in roles]
    # Obtener el rol del trabajador
    role = [role for role in roles if role['id'] == worker.role_id][0]
    # Crear el Json del trabajador
    worker_json = {
        'id': worker.id,
        'level': worker.level,
        'user': {
            'numeroDocumento': user.num_doc,
            'nombreCompleto': user.full_name,
            'email': user.email,
            'estado': user.is_active,
            'username': user.username
        },
        'role': {
            'id': role['id'],
            'descripcion': role['description'],
        }
    }
    return worker_json

@workers.put('/admin/actualizarRolTrabajador/{dni}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Actualizar el rol de un trabajador')
async def update_worker(dni: str, role_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    # Obtener el trabajador
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == dni).first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Trabajador no encontrado')
    # Actualizar el rol del trabajador
    worker.role_id = role_id
    db.commit()
    db.refresh(worker)

    # Obtener el usuario del trabajador
    user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
    # Obtener todos los roles
    roles = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 2).all()
    roles = [{'id': role.id_table, 'description': role.description} for role in roles]

    # Obtener el rol del trabajador
    role = [role for role in roles if role['id'] == worker.role_id][0]

    # Crear el Json del trabajador
    worker_json = {
        'id': worker.id,
        'level': worker.level,
        'user': {
            'numeroDocumento': user.num_doc,
            'nombreCompleto': user.full_name,
            'email': user.email,
            'estado': user.is_active,
            'username': user.username
        },
        'role': {
            'id': role['id'],
            'descripcion': role['description'],
        }
    }
    return worker_json
    
