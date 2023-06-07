from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
#!USER
from app.util.request import get_peruvian_card
from app.schemas.user import UserPost
from app.scripts.user import create_user
#!CLIENT
from app.models.client import Client as ClientModel

def create_user_client(db: Session, user: UserPost):
    client_data = get_peruvian_card(user.num_doc, user.type_doc)
    if 'nombre' not in client_data:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El numero de documento no existe")
    user_db = create_user(db, user, client_data['nombre'])
    client_db = ClientModel(
        user_id = user_db.num_doc,
        created_at = datetime.now(),
        last_connection = datetime.now()
    )
    db.add(client_db)
    db.commit()
    db.refresh(client_db)
    user_client = {'user': {'num_doc': user_db.num_doc, 'type_doc': user_db.type_doc, 'username': user_db.username, 'full_name': user_db.full_name, 'email': user_db.email, 'is_active': user_db.is_active}, 'client': {'user_id': client_db.user_id, 'created_at': client_db.created_at, 'last_connection': client_db.last_connection}}
    return user_client

