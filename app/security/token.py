from datetime import datetime, timedelta
import time
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
#!Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#!Security
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.db import get_db
#!USER
from app.models.user import User as UserModel
#!CLIENT
from app.models.client import Client as ClientModel
#!WORKER
from app.models.worker import Worker as WorkerModel
#!ADMIN
from app.models.admin import Admin as AdminModel

#!Poner la ruta desde donde se puede obtener el token en este caso /api/v1/public/login
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/public/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_reset_token(email: str):
    delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    data = {"email": email, "exp": expires}
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token



def send_email_to_reset_password(full_name:str,email: str, token: str):
    subject = "Recuperar contraseña"
    body = f"""
    Bievenido! Te saluda el equipo de desarrollo.

    Hola {full_name}, has solicitado recuperar tu contraseña.

    Para recuperar tu contraseña, te brindamos el siguiente token:
    Token = {token}
    """
    send_email(
        email,
        subject,
        body
    )
    return HTTPException(status_code=status.HTTP_200_OK, detail="Se ha enviado un correo electrónico con las instrucciones para recuperar tu contraseña")

def verify_password_reset_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = decoded_token.get("email")
        if email is None:
            return False
    except JWTError:
        return False
    return email


def get_password_hash(password: str):
    return pwd_context.hash(password)


def send_email_user_created(full_name: str, username: str, email: str, password: str):
    subject = "Usuario creado"
    body = f"""
    Bievenido! Te saluda el equipo de desarrollo.

    Hola {full_name}, se ha creado tu usuario.

    Tu usuario es: {username}
    Tu contraseña es: {password}
    
    Nota: 
        Por privacidad, la contraseña se ha encriptado. 
        Si la olvidas, deberás cambiarla.
    """
    send_email(
        email,
        subject,
        body
    )
    return HTTPException(status_code=status.HTTP_200_OK, detail="Se ha enviado un correo electrónico con los datos de tu usuario")

def send_email_user_updated_password(full_name: str, username: str, email: str, password: str):
    subject = "Usuario actualizado"
    body = f"""
    Bievenido! Te saluda el equipo de desarrollo.

    Hola {full_name}, se ha actualizado tu usuario.

    Tu usuario es: {username}
    Tu contraseña es: {password}
    
    Nota: 
        Por privacidad, la contraseña se ha encriptado. 
        Si la olvidas, deberás cambiarla.
    """
    send_email(
        email,
        subject,
        body
    )
    return HTTPException(status_code=status.HTTP_200_OK, detail="Se ha enviado un correo electrónico con los datos de tu usuario")

def send_email_user_updated_email(full_name: str, username: str, email: str):
    subject = "Usuario actualizado"
    body = f"""
    Bievenido! Te saluda el equipo de desarrollo.

    Hola {full_name}, se ha actualizado tu usuario.

    Tu usuario es: {username}
    Tu email es: {email}
    """
    send_email(
        email,
        subject,
        body
    )
    return HTTPException(status_code=status.HTTP_200_OK, detail="Se ha enviado un correo electrónico con los datos de tu usuario")    


def send_email(email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    text = msg.as_string()
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, email, text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al enviar el correo")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

token_registry = {}
blacklisted_tokens = set()

def create_access_token(username: str):
    existing_token = token_registry.get(username)
    if existing_token and is_token_active(existing_token):
        # El token existente aún es válido, devolverlo
        return {"access_token": existing_token, "token_type": "bearer"}
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    save_token(username, encoded_jwt)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

def is_token_active(token: str) -> bool:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire = datetime.fromtimestamp(decoded_token.get('exp'))
        if datetime.utcnow() < expire and token_not_blacklisted(token):
            return True
        #return False
    except JWTError:
        return None

def save_token(username: str, token: str):
    token_registry[username] = token

def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

def token_not_blacklisted(token: str):
    return token not in blacklisted_tokens

def get_current_user(db, token: str = Depends(oauth2_schema)) -> UserModel:
    data = decode_access_token(token)
    if data:
        current_time = time.time()
        if "exp" in data and current_time > data["exp"]:
            blacklisted_tokens.add(token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
        if not token_not_blacklisted(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})
        return db.query(UserModel).filter(UserModel.username == data["sub"]).first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})
    
def move_token_to_blacklist(token: str):
    blacklisted_tokens.add(token)
    username = get_username_from_token(token)
    if username in token_registry:
        del token_registry[username]

def get_username_from_token(token: str):
    data = decode_access_token(token)
    if data:
        return data.get("sub")
    return None


def get_current_active_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    #db = get_db()
    user_data = get_current_user(db, token)
    if user_data.is_active:
        user_type = get_type_user_by_num_doc(db, user_data.num_doc)
        user_type_map = {
            "client": ClientModel,
            "worker": WorkerModel,
            "admin": AdminModel
        }
        type_model = user_type_map[user_type]
        user_type_data = db.query(type_model).filter(
            type_model.user_id == user_data.num_doc).first()
        return {
            user_type: {
                "id": user_type_data.id,
                "tipoDocumento": user_data.type_doc,
                "numeroDocumento": user_data.num_doc,
                "nombreCompleto": user_data.full_name,
                "correoElectronico": user_data.email,
                "estadoUsuario": "Activo" if user_data.is_active else "Inactivo",
                "fechaCreacion": user_type_data.created_at,
                "ultimoInicioSesion": user_type_data.last_connection,
                "rol": None if user_type == "client" else user_type_data.role_id,
                "nivelAcceso": None if user_type == "client" else user_type_data.level
            },
            'access_token': token
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuario inactivo", headers={"WWW-Authenticate": "Bearer"})


def get_type_user_by_num_doc(db, num_doc: str):
    client = db.query(ClientModel).filter(
        ClientModel.user_id == num_doc).first()
    if client:
        return "client"
    worker = db.query(WorkerModel).filter(
        WorkerModel.user_id == num_doc).first()
    if worker:
        return "worker"
    admin = db.query(AdminModel).filter(AdminModel.user_id == num_doc).first()
    if admin:
        return "admin"
