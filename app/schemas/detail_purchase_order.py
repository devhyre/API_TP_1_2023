from pydantic import BaseModel, validator

class DetailPurchaseOrder(BaseModel):
    product_id: int
    quantity: int
    purchase_order_id: int

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
    
    @validator('purchase_order_id')
    def purchase_order_id_must_be_valid(cls, purchase_order_id):
        if purchase_order_id < 0:
            raise ValueError("La orden de compra debe ser válida")
        return purchase_order_id
    
class DetailPurchaseOrderPost(DetailPurchaseOrder):
    pass

class DetailPurchaseOrderPut(DetailPurchaseOrder):
    quantity: int

    @validator('quantity')
    def quantity_must_be_valid(cls, quantity):
        if quantity < 0:
            raise ValueError("La cantidad debe ser válida")
        return quantity
