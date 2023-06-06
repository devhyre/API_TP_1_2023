from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.util.request import get_peruvian_card
#!SUPPLIER
from app.models.supplier import Supplier as SupplierModel
from app.schemas.supplier import SupplierPost, SupplierPut

#!6 - RUC
#!1 - DNI

def create_supplier(db: Session, supplier: SupplierPost):
    supplier_data = get_peruvian_card(supplier.num_doc, 6)
    supplier_represenative_data = get_peruvian_card(supplier.num_doc_representative, 1)
    supplier_db = SupplierModel(
        num_doc = supplier.num_doc,
        name = supplier_data["nombre"],
        num_doc_representative = supplier.num_doc_representative,
        name_representative = supplier_represenative_data["nombre"],
        email = supplier.email,
        phone = supplier.phone,
        status = True
    )
    db.add(supplier_db)
    db.commit()
    db.refresh(supplier_db)
    return supplier_db

def update_supplier(db: Session, id_supplier: str, supplier: SupplierPut):
    """
    SOLO SE PUEDE ACTUALIZAR EL NUM_DOC_REPRESENTATIVE, EMAIL, PHONE
    """
    supplier_exists = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
    if not supplier_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El proveedor con id {id_supplier} no existe")
    else:
        name_representative = get_peruvian_card(supplier.num_doc_representative, 1)["nombre"]
        supplier_exists = SupplierModel(
            num_doc_representative = supplier.num_doc_representative,
            name_representative = name_representative,
            email = supplier.email,
            phone = supplier.phone
        )
        db.commit()
        db.refresh(supplier_exists)
        return supplier_exists

def update_status_supplier(db: Session, id_supplier: str):
    supplier = db.query(SupplierModel).filter(SupplierModel.num_doc == id_supplier).first()
    status = not supplier.status
    supplier.status = status
    db.commit()
    db.refresh(supplier)
    return supplier