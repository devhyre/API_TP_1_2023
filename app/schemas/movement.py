from datetime import datetime
from pydantic import BaseModel, validator

class Movement(BaseModel):
    sn_id: str
    worker_id: int
    created_at: str
    type_id: int

    @validator('sn_id')
    def sn_id_must_be_valid(cls, sn_id):
        if not sn_id.isalnum():
            raise ValueError("El número de serie solo puede contener caracteres alfanuméricos")
        return sn_id
    
    @validator('worker_id')
    def worker_id_must_be_valid(cls, worker_id):
        if worker_id < 0:
            raise ValueError("El trabajador debe ser válido")
        return worker_id
    
    @validator('type_id')
    def type_id_must_be_valid(cls, type_id):
        if type_id < 0:
            raise ValueError("El tipo de movimiento debe ser válido")
        return type_id
    
class MovementPost(Movement):
    pass

class MovementPut(Movement):
    pass