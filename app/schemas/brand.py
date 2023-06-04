from typing import Optional
from pydantic import BaseModel, validator

class Brand(BaseModel):
    name: str
    description: Optional[str] = None

    @validator('name')
    def name_must_be_valid(cls, name):
        if len(name) > 100:
            raise ValueError("El nombre debe tener máximo 100 caracteres")
        return name
    
    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description
    
class BrandPost(Brand):
    pass

class BrandPut(Brand):
    description: Optional[str] = None

    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description