from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.supplier import Supplier as SupplierModel
from app.schemas.supplier import SupplierPost, SupplierPut, Supplier
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user
from app.scripts.supplier import create_supplier, update_supplier, update_status_supplier

supplier = APIRouter()

@supplier.get('/listadoProveedores')
async def listar_proveedores(db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        suppliers = db.query(SupplierModel).all()
        return [supplier for supplier in suppliers]

@supplier.get('/obtenerProveedor/{num_doc}', response_model=Supplier)
async def obtener_proveedor(id_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type == 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
        return supplier

@supplier.post('/registrarProveedor', status_code=status.HTTP_201_CREATED)
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

@supplier.put('/actualizarProveedor/{id_supplier}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_proveedor(id_supplier: str, supplier: SupplierPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor {id_supplier} no existe")
        update = update_supplier(db, id_supplier, supplier)
        return update
    
@supplier.put('/actualizarProveedor/{id_supplier}/estado', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_estado_proveedor(id_supplier: str, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
        update = update_status_supplier(db, id_supplier)
        return update

@supplier.delete('/eliminarProveedor/{id_supplier}', status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proveedor(id_supplier: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        supplier_exists = db.query(SupplierModel).filter(SupplierModel.id_supplier == id_supplier).first()
        if not supplier_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
        db.query(SupplierModel).filter(SupplierModel.id_supplier == id_supplier).delete()
        db.commit()
        return {'message': f'Proveedor con id {id_supplier} eliminado'}
