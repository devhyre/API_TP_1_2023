from pydantic import BaseModel, validator
from datetime import datetime

class Combo(BaseModel):
    product_id: int
    created_at: datetime
    worker_id: int

    @validator('product_id')
    def product_id_must_be_valid(cls, product_id):
        if product_id < 0:
            raise ValueError("El producto debe ser válido")
        return product_id
    
    @validator('worker_id')
    def worker_id_must_be_valid(cls, worker_id):
        if worker_id < 0:
            raise ValueError("El trabajador debe ser válido")
        return worker_id
    
class ComboPost(Combo):
    pass

class ComboPut(Combo):
    pass