from sqlalchemy import Column, Integer, Boolean
from app.core.db import Base

class RolePrivilege(Base):
    __tablename__ = "role_privileges"

    role_id = Column(Integer, index=True, primary_key=True)
    module_1 = Column(Boolean, default=False)
    module_2 = Column(Boolean, default=False)
    module_3 = Column(Boolean, default=False)
    module_4 = Column(Boolean, default=False)
    module_5 = Column(Boolean, default=False)
    module_6 = Column(Boolean, default=False)
    module_7 = Column(Boolean, default=False)
    module_8 = Column(Boolean, default=False)
    module_9 = Column(Boolean, default=False)
    module_10 = Column(Boolean, default=False)
    module_11 = Column(Boolean, default=False)
    module_12 = Column(Boolean, default=False)
    module_13 = Column(Boolean, default=False)
    module_14 = Column(Boolean, default=False)
    module_15 = Column(Boolean, default=False)
    module_16 = Column(Boolean, default=False)
    module_17 = Column(Boolean, default=False)
    module_18 = Column(Boolean, default=False)
    module_19 = Column(Boolean, default=False)
    module_20 = Column(Boolean, default=False)