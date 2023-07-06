from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
#!SECURITY
from app.security.token import get_password_hash, get_type_user_by_num_doc, send_email_user_created, send_email_user_updated_email, send_email_user_updated_password
#!USER
from app.schemas.user import UserPost
from app.models.user import User as UserModel
#!CLIENT
from app.models.client import Client as ClientModel
#!WORKER
from app.models.worker import Worker as WorkerModel
#!ADMIN
from app.models.admin import Admin as AdminModel

def create_user(db: Session, user: UserPost, full_name: str):
    user_db = UserModel(
        num_doc = user.num_doc,
        type_doc = user.type_doc,
        username = user.username,
        full_name = full_name,
        email = user.email,
        password = get_password_hash(user.password),
        is_active = True
    )
    send_email_user_created(full_name, user.username, user.email, user.password)
    db.add(user_db)
    return user_db

def get_user_by_username(db, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_num_doc_username_email(db, num_doc: str, username: str, email: str):
    num_doc_exists = db.query(UserModel).filter(UserModel.num_doc == num_doc).first()
    username_exists = db.query(UserModel).filter(UserModel.username == username).first()
    email_exists = db.query(UserModel).filter(UserModel.email == email).first()
    if num_doc_exists or username_exists or email_exists:
        return True

def update_email(db, num_doc: str, email: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        user = change_email(db, num_doc, email)
        return user
    else:
        if user.num_doc == num_doc:
            user = change_email(db, num_doc, email)
            return user
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya le pertenece a otro usuario")
        
def change_email(db, num_doc: str, email: str):
    #Obtener el usuario
    db.query(UserModel).filter(UserModel.num_doc == num_doc).update({UserModel.email: email})
    db.commit()
    user = db.query(UserModel).filter(UserModel.num_doc == num_doc).first()
    send_email_user_updated_email(user.full_name, user.username, email)
    return user

def update_password(db, num_doc: str, password: str):
    db.query(UserModel).filter(UserModel.num_doc == num_doc).update({UserModel.password: get_password_hash(password)})
    db.commit()
    user = db.query(UserModel).filter(UserModel.num_doc == num_doc).first()
    send_email_user_updated_password(user.full_name, user.username, user.email, password)
    return user

def update_status(db, num_doc: str):
    db.query(UserModel).filter(UserModel.num_doc == num_doc).update({UserModel.is_active: not UserModel.is_active})
    db.commit()
    return True

def update_last_connection(db, num_doc: str):
    user_type = get_type_user_by_num_doc(db, num_doc)
    user_type_map = {
            "client": ClientModel,
            "worker": WorkerModel,
            "admin": AdminModel
        }
    type_model = user_type_map[user_type]
    db.query(type_model).filter(type_model.user_id == num_doc).update({type_model.last_connection: datetime.now()})
    db.commit()