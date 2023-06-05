from pydantic import BaseModel, validator

class Model(BaseModel):
    name: str
    description: str
    brand_id: int

    
    
    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description
    
    @validator('brand_id')
    def brand_id_must_be_valid(cls, brand_id):
        if brand_id < 0:
            raise ValueError("La marca debe ser válida")
        return brand_id
    
class ModelPost(Model):
    pass

class ModelPut(Model):
    name: str
    description: str

    @validator('name')
    def name_must_be_valid(cls, name):
        if len(name) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return name

    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener máximo 255 caracteres")
        return description