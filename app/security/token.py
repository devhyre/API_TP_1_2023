from datetime import datetime, timedelta
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
from app.core.db import get_db_session
#!USER
from app.models.user import User as UserModel
#!CLIENT
from app.models.client import Client as ClientModel
#!WORKER
from app.models.worker import Worker as WorkerModel
#!ADMIN
from app.models.admin import Admin as AdminModel
#!TABLE OF TABLES
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

#!Poner la ruta desde donde se puede obtener el token en este caso /api/v1/public/login
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/public/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, email, text)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al enviar el correo")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print('Token generado: ' + encoded_jwt + '\n' + 'Expira: ' + str(expire) + '\n' + 'Usuario: ' + username)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


blacklisted_tokens = set()

def get_current_user(db, token: str = Depends(oauth2_schema)) -> UserModel:
    print(token)
    data = decode_access_token(token)
    if data:
        """
        if token in blacklisted_tokens:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})
                                """
        return db.query(UserModel).filter(UserModel.username == data["sub"]).first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})


def get_current_active_user(token: str = Depends(oauth2_schema)):
    db: Session = get_db_session()
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
