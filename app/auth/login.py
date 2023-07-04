from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.scripts.user import get_user_by_username, update_last_connection, update_password
from app.security.token import verify_password, create_access_token, get_current_active_user, generate_password_reset_token, send_email_to_reset_password, verify_password_reset_token,move_token_to_blacklist
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User as UserModel
from app.schemas.user import UserPutPassword

auth = APIRouter()

@auth.post('/login', name='Iniciar sesión', status_code=status.HTTP_200_OK)
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

@auth.get('/logout', name='Cerrar sesión', status_code=status.HTTP_200_OK)
async def logout(response: Response, user: dict = Depends(get_current_active_user)):
    access_token = user.get("access_token")
    move_token_to_blacklist(access_token)  # Mover el token a la lista negra
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='username')
    response.delete_cookie(key='num_doc')
    return {'message': 'Logout exitoso'}

@auth.post('/forgot-password', status_code=status.HTTP_200_OK, name='Obtener token para restablecer contraseña')
async def forgot_password(email: str, db: Session = Depends(get_db)):
    # Validar que el email exista en la base de datos
    user_db = db.query(UserModel).filter(UserModel.email == email).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email no registrado')
    #! Generar un token de recuperación de contraseña
    token = generate_password_reset_token(email)
    #! Enviar un email con el token
    send_email_to_reset_password(user_db.full_name, email, token)
    return {'message': 'Email enviado'}

@auth.post('/reset-password/{token}', status_code=status.HTTP_200_OK, name='Validar token y actualizar contraseña')
async def reset_password(token: str, user_data: UserPutPassword, db: Session = Depends(get_db)):
    # Validar que el token sea válido
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Token inválido')
    # Validar que el email exista en la base de datos
    user_db = db.query(UserModel).filter(UserModel.email == email).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email no registrado')
    # Actualizar la contraseña
    update_password(db, user_db.num_doc, user_data.password)
    return {'message': 'Contraseña actualizada'}