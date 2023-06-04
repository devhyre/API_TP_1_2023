from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.supplier_category import SupplierCategory as SupplierCategoryModel
from app.schemas.supplier_category import SupplierCategory, SupplierCategoryPost
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

supplier_categories = APIRouter()

@supplier_categories.get('/listadoCategoriasProveedor', response_model=List[SupplierCategory])
async def listar_categorias_proveedor(db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_categories = db.query(SupplierCategoryModel).all()
        return supplier_categories
    
@supplier_categories.get('/obtenerCategoriasProveedor/{num_doc_supplier}')
async def obtener_categoria_proveedor(num_doc_supplier: str, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_categories = db.query(SupplierCategoryModel).filter(SupplierCategoryModel.num_doc_supplier == num_doc_supplier).all()
        return [{'id_supplier': supplier_category.supplier_id, 'id_category': supplier_category.category_id} for supplier_category in supplier_categories]
    
@supplier_categories.post('/registrarCategoriaProveedor')
async def registrar_categoria_proveedor(supplier_category: SupplierCategoryPost, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_category_db = SupplierCategoryModel(**supplier_category.dict())
        db.add(supplier_category_db)
        db.commit()
        db.refresh(supplier_category_db)
        return {'id_supplier': supplier_category_db.supplier_id, 'id_category': supplier_category_db.category_id}
    
@supplier_categories.delete('/eliminarCategoriaProveedor/{num_doc_supplier}/{id_category}')
async def eliminar_categoria_proveedor(num_doc_supplier: str, id_category: int, db: Session = Depends(get_db), user: ProfileResponse = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        db.query(SupplierCategoryModel).filter(SupplierCategoryModel.num_doc_supplier == num_doc_supplier, SupplierCategoryModel.category_id == id_category).delete()
        db.commit()
        return {'message': 'Se eliminó la categoría del proveedor'}