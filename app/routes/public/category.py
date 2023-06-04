from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

categories_pu = APIRouter()

@categories_pu.get('/listadoCategorias')
async def listar_categorias(db: Session = Depends(get_db)):
    categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
    return [{'id': category.id_table, 'description': category.description} for category in categories]
    
@categories_pu.get('/obtenerCategoria/{id_table}')
async def obtener_categoria(id_table: int, db: Session = Depends(get_db)):
    category = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3 and TableOfTablesModel.id_table == id_table).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con id {id_table} no existe")
    return {'id': category.id_table, 'description': category.description}

    