from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.user import UserPost
from app.scripts.user import get_user_by_num_doc_username_email
from app.scripts.client import create_user_client

register_client = APIRouter()


@register_client.post('/registrarCliente')
async def register(client: UserPost, db: Session = Depends(get_db)):
    client_exists = get_user_by_num_doc_username_email(db, client.num_doc, client.username, client.email)
    if client_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='El DNI, email o username ya esta registrado')
    create_user_client(db, client)
    return HTTPException(status_code=status.HTTP_201_CREATED, detail='Cliente creado')
        



"""
PROBANDO EN PONER ENDPOINT RESTRINGIDO
@register_client.post('/registrarCliente')
async def register(db: Session = Depends(get_db),token: str = Depends(oauth2_schema)):
    return {"token": token}
"""