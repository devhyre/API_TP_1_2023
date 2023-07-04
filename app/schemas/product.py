from pydantic import BaseModel, validator

class Product(BaseModel):
    name: str
    description: str
    path_image: str
    quantity: int
    price: float
    discount: int
    warranty: int
    category_id: int
    brand_id: int
    model_id: int
    status_id: int
    ranking: int

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
    
    @validator('path_image')
    def path_image_must_be_valid(cls, path_image):
        if len(path_image) > 100:
            raise ValueError("La ruta de la imagen debe tener máximo 100 caracteres")
        return path_image
    
    @validator('quantity')
    def quantity_must_be_valid(cls, quantity):
        if quantity < 0:
            raise ValueError("La cantidad debe ser válida")
        return quantity
    
    @validator('price')
    def price_must_be_valid(cls, price):
        if price < 0.0:
            raise ValueError("El precio debe ser válido")
        return price
    
    @validator('category_id')
    def category_id_must_be_valid(cls, category_id):
        if category_id < 0:
            raise ValueError("La categoría debe ser válida")
        return category_id
    
    @validator('brand_id')
    def brand_id_must_be_valid(cls, brand_id):
        if brand_id < 0:
            raise ValueError("La marca debe ser válida")
        return brand_id
    
    @validator('model_id')
    def model_id_must_be_valid(cls, model_id):
        if model_id < 0:
            raise ValueError("El modelo debe ser válido")
        return model_id
    
    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id
    
class ProductPost(Product):
    pass

class ProductPut(BaseModel):
    name: str
    description: str
    path_image: str
    price: float
    discount: int
    warranty: int
    status_id: int

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
    
    @validator('path_image')
    def path_image_must_be_valid(cls, path_image):
        if len(path_image) > 100:
            raise ValueError("La ruta de la imagen debe tener máximo 100 caracteres")
        return path_image
    
    @validator('price')
    def price_must_be_valid(cls, price):
        if price < 0.0:
            raise ValueError("El precio debe ser válido")
        return price
    
    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id