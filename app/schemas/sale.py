from pydantic import BaseModel, validator
from datetime import datetime

class Sale(BaseModel):
    order_id: int
    user_id: str
    code_payment: str
    created_at: datetime
    total: float

    @validator('order_id')
    def order_id_must_be_valid(cls, order_id):
        if order_id < 0:
            raise ValueError("El pedido debe ser válido")
        return order_id
    
    @validator('user_id')
    def user_id_must_be_valid(cls, user_id):
        if user_id.isdigit() == False:
            raise ValueError("El usuario debe ser válido")
        return user_id
    
    @validator('total')
    def total_must_be_valid(cls, total):
        if total < 0.0:
            raise ValueError("El total debe ser válido")
        return total

class SalePost(Sale):
    code_payment: str
    created_at: datetime
    total: float

class SalePut(BaseModel):
    code_payment: str