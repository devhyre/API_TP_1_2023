from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.scripts.user import get_user_by_username, update_last_connection
from app.security.token import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

auth = APIRouter()

@auth.post('/login')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_exists = get_user_by_username(db, user.username)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no registrado')
    if not verify_password(user.password, user_exists.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contraseña incorrecta')
    if not user_exists.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario inactivo')
    access_token = create_access_token(user.username)
    response = Response()
    response.set_cookie(key='access_token', value=access_token)
    response.set_cookie(key='username', value=user.username)
    response.set_cookie(key='num_doc', value=user_exists.num_doc)
    update_last_connection(db, user_exists.num_doc)
    return access_token

@auth.get('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='username')
    response.delete_cookie(key='num_doc')
    return {'message': "Sesión cerrada correctamente"}