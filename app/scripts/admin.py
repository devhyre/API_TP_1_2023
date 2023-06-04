from sqlalchemy.orm import Session
from datetime import datetime
#!USER
from app.util.request import get_peruvian_card
from app.schemas.user import UserPost
from app.scripts.user import create_user
#!ADMIN
from app.models.admin import Admin as AdminModel
from app.schemas.admin import AdminPost

def create_user_admin(db: Session, user: UserPost, role_id: int, level: int):
    admin_data = get_peruvian_card(user.num_doc, user.type_doc)
    user_db = create_user(db, user, admin_data['nombre'])
    admin_db = AdminModel(
        user_id = user_db.num_doc,
        created_at = datetime.now(),
        last_connection = datetime.now(),
        role_id = role_id,
        level = level
    )
    db.add(admin_db)
    db.commit()
    db.refresh(admin_db)
    user_admin = {'user': {'num_doc': user_db.num_doc, 'type_doc': user_db.type_doc, 'username': user_db.username, 'full_name': user_db.full_name, 'email': user_db.email, 'is_active': user_db.is_active}, 'admin': {'user_id': admin_db.user_id, 'created_at': admin_db.created_at, 'last_connection': admin_db.last_connection, 'role_id': admin_db.role_id, 'level': admin_db.level}}
    return user_admin