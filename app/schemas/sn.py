from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime

class SerialNumber(BaseModel):
    sn_id: str
    product_id: int
    supplier_id: str
    user_id: str
    status_id: int
    entrance_at: datetime
    departure_at: Optional[datetime] = None

    @validator('sn_id')
    def serial_number_must_be_valid(cls, serial_number):
        if not serial_number.isalnum():
            raise ValueError("El serial debe ser válido")
        return serial_number
    
    @validator('product_id')
    def product_id_must_be_valid(cls, product_id):
        if product_id < 0:
            raise ValueError("El producto debe ser válido")
        return product_id
    
    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id
    
class SerialNumberPost(SerialNumber):
    pass

class SerialNumberPut(SerialNumber):
    status_id: int
    departure_at: datetime

    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id