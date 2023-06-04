from sqlalchemy.orm import Session
from datetime import datetime
#!USER
from app.util.request import get_peruvian_card
from app.schemas.user import UserPost
from app.scripts.user import create_user
#!WORKER
from app.models.worker import Worker as WorkerModel

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