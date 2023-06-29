from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.supplier import Supplier as SupplierModel
from app.schemas.supplier import SupplierPost, SupplierPut
from app.security.token import get_current_active_user
from app.scripts.supplier import create_supplier, update_supplier, update_status_supplier

supplier = APIRouter()

@supplier.get('/admin/listadoProveedores',name='ADMINISTRADOR|TRABAJADOR - Obtener todos los proveedores', status_code=status.HTTP_200_OK)
async def listar_proveedores(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        # Crear el Json de respuesta
        response = []
        # Obtener los proveedores
        suppliers = db.query(SupplierModel).all()
        # Recorrer los proveedores
        for supplier in suppliers:
            # Crear el Json del proveedor
            supplier_json = {
                'razon_social': supplier.num_doc,
                'nombre': supplier.name,
                'numero_documeto_representante': supplier.num_doc_representative,
                'nombre_representante': supplier.name_representative,
                'telefono': supplier.phone,
                'email': supplier.email,
                'estado': supplier.status
            }
            # Agregar el Json del proveedor al Json de respuesta
            response.append(supplier_json)
        # Retornar el Json de respuesta
        return response

@supplier.get('/admin/obtenerProveedor/{num_doc}', status_code=status.HTTP_200_OK, name='ADMINISTRADOR|TRABAJADOR - Obtener un proveedor por id')
async def obtener_proveedor(id_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El proveedor no existe')
        # Crear el Json del proveedor
        supplier_json = {
            'razon_social': supplier.num_doc,
            'nombre': supplier.name,
            'numero_documeto_representante': supplier.num_doc_representative,
            'nombre_representante': supplier.name_representative,
            'telefono': supplier.phone,
            'email': supplier.email,
            'estado': supplier.status
        }
        # Retornar el Json del proveedor
        return supplier_json

@supplier.post('/admin/registrarProveedor', status_code=status.HTTP_201_CREATED, name='ADMINISTRADOR|TRABAJADOR - Registrar un proveedor')
async def registrar_proveedor(supplier: SupplierPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == supplier.num_doc).first()
        if supplier_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='El proveedor ya esta registrado')
        db_supplier = create_supplier(db, supplier)
        return db_supplier

@supplier.put('/admin/actualizarProveedor/{id_supplier}', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR - Actualizar un proveedor')
async def actualizar_proveedor(id_supplier: str, supplier: SupplierPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor {id_supplier} no existe")
        update = update_supplier(db, id_supplier, supplier)
        # Crear el Json del proveedor
        supplier_json = {
            'razon_social': update.num_doc,
            'nombre': update.name,
            'numero_documeto_representante': update.num_doc_representative,
            'nombre_representante': update.name_representative,
            'telefono': update.phone,
            'email': update.email,
            'estado': update.status
        }
        # Retornar el Json del proveedor
        return supplier_json
        
    
@supplier.put('/admin/actualizarProveedor/{id_supplier}/estado', status_code=status.HTTP_202_ACCEPTED, name='ADMINISTRADOR - Actualizar el estado de un proveedor')
async def actualizar_estado_proveedor(id_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
        update = update_status_supplier(db, id_supplier)
        # Crear el Json del proveedor
        supplier_json = {
            'razon_social': update.num_doc,
            'nombre': update.name,
            'numero_documeto_representante': update.num_doc_representative,
            'nombre_representante': update.name_representative,
            'telefono': update.phone,
            'email': update.email,
            'estado': update.status
        }
        # Retornar el Json del proveedor
        return supplier_json

@supplier.delete('/admin/eliminarProveedor/{id_supplier}', status_code=status.HTTP_204_NO_CONTENT, name='ADMINISTRADOR - Eliminar un proveedor')
async def eliminar_proveedor(id_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
        db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).delete()
        db.commit()
        return {'message': f'Proveedor con id {id_supplier} eliminado'}
