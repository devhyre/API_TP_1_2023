from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
#!USER
from app.util.request import get_peruvian_card
from app.schemas.user import UserPost
from app.scripts.user import create_user
#!WORKER
from app.models.worker import Worker as WorkerModel
#!USER
from app.models.user import User as UserModel

def create_user_worker(db: Session, user: UserPost, role_id: int, level: int):
    worker_data = get_peruvian_card(user.num_doc, user.type_doc)
    user_db = create_user(db, user, worker_data['nombre'])
    worker_db = WorkerModel(
        user_id = user_db.num_doc,
        created_at = datetime.now(),
        last_connection = datetime.now(),
        role_id = role_id,
        level = level
    )
    db.add(worker_db)
    db.commit()
    db.refresh(worker_db)
    user_worker = {'user': {'num_doc': user_db.num_doc, 'type_doc': user_db.type_doc, 'username': user_db.username, 'full_name': user_db.full_name, 'email': user_db.email, 'is_active': user_db.is_active}, 'worker': {'user_id': worker_db.user_id, 'created_at': worker_db.created_at, 'last_connection': worker_db.last_connection, 'role_id': worker_db.role_id, 'level': worker_db.level}}
    return user_worker

def get_all_workers(db: Session): #MI CEREBRO SE APAGO, SI ESTA BIEN, NICE XD
    workers = db.query(WorkerModel).all()
    #!Lista para almacenar los trabajadores con sus datos de usuario
    result = []
    #!Obtener los datos de usuario para cada trabajador
    for worker in workers:
        user = db.query(UserModel).filter(UserModel.num_doc == worker.user_id).first()
        #!Crear un diccionario con los datos del trabajador y el usuario
        worker_data = {
            "worker": worker,
            "user": user
        }
        result.append(worker_data)
    return result

def update_role_worker(db: Session, worker_id: str, role_id: int):
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El trabajador no existe')
    worker.role_id = role_id
    db.commit()
    return {'message': 'Rol actualizado'}

def get_worker_by_id(db: Session, worker_id: str):
    worker = db.query(WorkerModel).filter(WorkerModel.user_id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El trabajador no existe')
    user = db.query(UserModel).filter(UserModel.num_doc == worker_id).first()
    worker_data = {
        "worker": worker,
        "user": user
    }
    return worker_data
