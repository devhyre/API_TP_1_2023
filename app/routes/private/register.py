from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.user import UserPost
from app.scripts.user import get_user_by_num_doc_username_email
from app.scripts.worker import create_user_worker
from app.scripts.admin import create_user_admin
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

register = APIRouter()

@register.post('/registrarTrabajador', status_code=status.HTTP_201_CREATED)
async def register_worker(worker: UserPost, role_id: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para registrar un trabajador')
    else:
        worker_exists = get_user_by_num_doc_username_email(db, worker.num_doc, worker.username, worker.email)
        if worker_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='El DNI, email o username ya esta registrado')
        if role_id == 0 or role_id == 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El rol no es valido')
        create_user_worker(db, worker, role_id, 0)
        return {'message': 'Trabajador creado'}
    
@register.post('/registrarAdministrador', status_code=status.HTTP_201_CREATED)
async def register_admin(admin: UserPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para registrar un administrador')
    else:
        admin_exists = get_user_by_num_doc_username_email(db, admin.num_doc, admin.username, admin.email)
        if admin_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='El DNI, email o username ya esta registrado')
        create_user_admin(db, admin, 1, 5)
        return {'message': 'Administrador creado'}