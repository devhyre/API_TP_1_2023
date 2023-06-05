from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.scripts.worker import get_all_workers, get_worker_by_id, update_role_worker

workers = APIRouter()

@workers.get('/obtenerTrabajadores', status_code=status.HTTP_200_OK)
async def get_workers(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    workers = get_all_workers(db)
    return workers

@workers.get('/obtenerTrabajador/{dni}', status_code=status.HTTP_200_OK)
async def get_worker(dni: str, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    worker = get_worker_by_id(db, dni)
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Trabajador no encontrado')
    return worker

@workers.put('/actualizarRolTrabajador/{dni}', status_code=status.HTTP_200_OK)
async def update_worker(dni: str, role_id: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')
    update_role_worker(db, dni, role_id)
    return {'message': 'Rol actualizado'}
