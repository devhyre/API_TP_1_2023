from fastapi import APIRouter, Depends, status
from app.core.db import Session, get_db
from app.scripts.user import update_email, update_password
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.schemas.user import UserPutEmail, UserPutPassword

profile = APIRouter()

@profile.get('/obtenerPerfil', response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile(user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    return ProfileResponse(
        id=user[user_type]['id'],
        tipoDocumento=user[user_type]['tipoDocumento'],
        numeroDocumento=user[user_type]['numeroDocumento'],
        nombreCompleto=user[user_type]['nombreCompleto'],
        correoElectronico=user[user_type]['correoElectronico'],
        estadoUsuario=user[user_type]['estadoUsuario'],
        fechaCreacion=user[user_type]['fechaCreacion'],
        ultimoInicioSesion=user[user_type]['ultimoInicioSesion'],
        rol=user[user_type]['rol'],
        nivelAcceso=user[user_type]['nivelAcceso']
    )

@profile.put('/actualizarEmail', response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def put_email(user_data: UserPutEmail, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_update = update_email(db, user['client']['numeroDocumento'], user_data.email)
    user_type = list(user.keys())[0]
    return ProfileResponse(
        id=user[user_type]['id'],
        tipoDocumento=user[user_type]['tipoDocumento'],
        numeroDocumento=user[user_type]['numeroDocumento'],
        nombreCompleto=user[user_type]['nombreCompleto'],
        correoElectronico=user_update.email,
        estadoUsuario=user[user_type]['estadoUsuario'],
        fechaCreacion=user[user_type]['fechaCreacion'],
        ultimoInicioSesion=user[user_type]['ultimoInicioSesion'],
        rol=user[user_type]['rol'],
        nivelAcceso=user[user_type]['nivelAcceso']
    )

@profile.put('/actualizarPassword', status_code=status.HTTP_200_OK)
async def put_password(user_data: UserPutPassword, user: ProfileResponse = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_type = list(user.keys())[0]
    update_password(db, user[user_type]['numeroDocumento'], user_data.password)
    return {'message': 'Contraseña actualizada'}
    

