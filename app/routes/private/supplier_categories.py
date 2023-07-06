from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.supplier_category import SupplierCategory as SupplierCategoryModel
from app.schemas.supplier_category import SupplierCategory, SupplierCategoryPost
from app.security.token import get_current_active_user
from app.models.supplier import Supplier as SupplierModel
from app.models.table_of_tables import TableOfTables as TableOfTablesModel

supplier_categories = APIRouter()

@supplier_categories.get('/admin/listadoCategoriasProveedor', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Listar categorias de proveedores')
async def listar_categorias_proveedor(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener las categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = sorted(categories, key=lambda x: x.id_table)
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Obtener los proveedores
        suppliers = db.query(SupplierModel).all()

        # Obtener las categorias de los proveedores
        supplier_categories = db.query(SupplierCategoryModel).all()

        # Crear el Json de respuesta
        response = []

        # Recorrer los proveedores y agregar las categorias
        for supplier in suppliers:
            # Crear el Json del proveedor con sus categorias
            supplier_json = {
                'razon_social': supplier.num_doc,
                'nombre': supplier.name,
                'numero_documeto_representante': supplier.num_doc_representative,
                'nombre_representante': supplier.name_representative,
                'telefono': supplier.phone,
                'email': supplier.email,
                'estado': supplier.status,
                'categorias': []
            }
            for supplier_category in supplier_categories:
                if supplier_category.supplier_id == supplier.num_doc:
                    # Obtener la categoria
                    category = next((category for category in categories if category['id'] == supplier_category.category_id), None)
                    # Crear el Json de la categoria
                    category_json = {
                        'id': category['id'],
                        'description': category['description']
                    }
                    # Agregar la categoria al proveedor
                    supplier_json['categorias'].append(category_json)
            # Agregar el proveedor a la respuesta
            response.append(supplier_json)
        return response          
    
@supplier_categories.get('/admin/obtenerCategoriasProveedor/{num_doc_supplier}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener categorias de un proveedor')
async def obtener_categoria_proveedor(num_doc_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Obtener las categorias del proveedor
        supplier_categories = db.query(SupplierCategoryModel).filter(SupplierCategoryModel.num_doc_supplier == num_doc_supplier).all()
        # Obtener las categorias
        categories = db.query(TableOfTablesModel).filter(TableOfTablesModel.id == 3).all()
        categories = sorted(categories, key=lambda x: x.id_table)
        categories = [{'id': category.id_table, 'description': category.description} for category in categories]
        # Crear el Json de respuesta
        response = []
        # Recorrer las categorias del proveedor y agregarlas a la respuesta
        for supplier_category in supplier_categories:
            # Obtener la categoria
            category = next((category for category in categories if category['id'] == supplier_category.id_category), None)
            # Crear el Json de la categoria
            category_json = {
                'id': category['id'],
                'description': category['description']
            }
            # Agregar la categoria a la respuesta
            response.append(category_json)
        return response

@supplier_categories.post('/admin/registrarCategoriaProveedor', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR - Registrar categoria de proveedor')
async def registrar_categoria_proveedor(supplier_category: SupplierCategoryPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_category_db = SupplierCategoryModel(**supplier_category.dict())
        db.add(supplier_category_db)
        db.commit()
        db.refresh(supplier_category_db)
        return {'message': 'Se registró la categoría del proveedor', 'data': supplier_category_db}
    
@supplier_categories.delete('/admin/eliminarCategoriaProveedor/{num_doc_supplier}/{id_category}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR - Eliminar categoria de proveedor')
async def eliminar_categoria_proveedor(num_doc_supplier: str, id_category: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        db.query(SupplierCategoryModel).filter(SupplierCategoryModel.supplier_id == num_doc_supplier, SupplierCategoryModel.category_id == id_category).delete()
        db.commit()
        return {'message': 'Se eliminó la categoría del proveedor'}