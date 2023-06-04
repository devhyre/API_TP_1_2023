from pydantic import BaseModel, validator
from datetime import datetime

class OrderGuide(BaseModel):
    order_id: int
    created_at: datetime

    @validator('order_id')
    def order_id_must_be_valid(cls, order_id):
        if order_id < 0:
            raise ValueError("El pedido debe ser válido")
        return order_id
    
class OrderGuidePost(OrderGuide):
    pass

class OrderGuidePut(OrderGuide):
    pass
