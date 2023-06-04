from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(12), ForeignKey("users.num_doc"), index=True)
    created_at = Column(DateTime)
    last_connection = Column(DateTime)
    role_id = Column(Integer)
    #0: Lectura, 1: Escritura, 2: Lectura y Escritura, 3: Lectura, Escritura y Edicion, 4: Lectura, Escritura, Edicion y Eliminacion
    level = Column(Integer, default=0)

    user = relationship("User", foreign_keys=[user_id])