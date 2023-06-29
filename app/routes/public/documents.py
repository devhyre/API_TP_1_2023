from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.table_of_tables import TableOfTables as TableOfTablesModel


documents = APIRouter()

@documents.get('/listadoDocumentos', status_code=status.HTTP_200_OK, name='Listado de documentos')
async def listar_documentos(db: Session = Depends(get_db)):
    documents = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 1).all()
    documents = sorted(documents, key=lambda x: x.id_table)
    return [{'id': document.id_table, 'description': document.description} for document in documents]

@documents.get('/obtenerDocumento/{id_table}', status_code=status.HTTP_200_OK, name='Obtener documento')
async def obtener_documento(id_table: int, db: Session = Depends(get_db)):
    document = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 1 and TableOfTablesModel.id_table == id_table).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El documento con id {id_table} no existe")
    return {'id': document.id_table, 'description': document.description}