from pydantic import BaseModel, validator

class DetailOrder(BaseModel):
    order_id: int
    product_id: int
    quantity: int

    @validator('order_id')
    def order_id_must_be_valid(cls, order_id):
        if order_id < 0:
            raise ValueError("El pedido debe ser válido")
        return order_id
    
    @validator('product_id')
    def product_id_must_be_valid(cls, product_id):
        if product_id < 0:
            raise ValueError("El producto debe ser válido")
        return product_id
    
    @validator('quantity')
    def quantity_must_be_valid(cls, quantity):
        if quantity < 0:
            raise ValueError("La cantidad debe ser válida")
        return quantity
    
class DetailOrderPost(DetailOrder):
    pass

class DetailOrderPut(DetailOrder):
    quantity: int

    @validator('quantity')
    def quantity_must_be_valid(cls, quantity):
        if quantity < 0:
            raise ValueError("La cantidad debe ser válida")
        return quantity