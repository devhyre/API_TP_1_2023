from sqlalchemy import Column, Integer, String
from app.core.db import Base

Base.metadata.schema

class TableOfTables(Base):
    __tablename__ = "table_of_tables"

    id = Column(Integer, index=True)
    id_table = Column(Integer, index=True)
    description = Column(String(255), nullable=False,  index=True, primary_key=True)