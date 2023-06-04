from pydantic import BaseModel, validator
from datetime import datetime

class Order(BaseModel):
    user_id: str
    created_at: datetime
    discount: int
    status_order: int

    @validator('user_id')
    def user_id_must_be_valid(cls, user_id):
        if user_id.isdigit() == False:
            raise ValueError("El usuario debe ser válido")
        return user_id
    
class OrderPost(Order):
    pass

class OrderPut(Order):
    pass