from pydantic import BaseModel, validator

class DetailCombo(BaseModel):
    product_id: int
    quantity: int
    
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
    
class DetailComboPost(DetailCombo):
    pass

class DetailComboPut(DetailCombo):
    quantity: int

    @validator('quantity')
    def quantity_must_be_valid(cls, quantity):
        if quantity < 0:
            raise ValueError("La cantidad debe ser válida")
        return quantity