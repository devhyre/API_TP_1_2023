from pydantic import BaseModel, validator
from datetime import datetime

class PurchaseOrder(BaseModel):
    supplier_id: int
    worker_id: int
    created_at: datetime

    @validator('supplier_id')
    def supplier_id_must_be_valid(cls, supplier_id):
        if supplier_id < 0:
            raise ValueError("El proveedor debe ser válido")
        return supplier_id
    
    @validator('worker_id')
    def worker_id_must_be_valid(cls, worker_id):
        if worker_id < 0:
            raise ValueError("El trabajador debe ser válido")
        return worker_id
    
class PurchaseOrderPost(PurchaseOrder):
    pass

class PurchaseOrderPut(PurchaseOrder):
    pass