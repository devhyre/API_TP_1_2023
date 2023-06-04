from typing import Optional
from pydantic import BaseModel, validator

class Assembly(BaseModel):
    major_product_id: int
    product_id: int
    description: Optional[str] = None

    @validator('major_product_id')
    def major_product_id_must_be_valid(cls, major_product_id):
        if major_product_id < 0:
            raise ValueError("El producto mayor debe ser válido")
        return major_product_id
    
    @validator('product_id')
    def product_id_must_be_valid(cls, product_id):
        if product_id < 0:
            raise ValueError("El producto debe ser válido")
        return product_id
    
    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description
    
class AssemblyPost(Assembly):
    pass
    
class AssemblyPut(Assembly):
    description: Optional[str] = None

    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description
