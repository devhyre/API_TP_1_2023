from pydantic import BaseModel, validator

class SupplierCategory(BaseModel):
    category_id: int
    supplier_id: str

    @validator('category_id')
    def category_id_must_be_valid(cls, category_id):
        if category_id < 0:
            raise ValueError("La categoría debe ser válida")
        return category_id
    
    @validator('supplier_id')
    def supplier_id_must_be_valid(cls, supplier_id):
        if not supplier_id.isnumeric():
            raise ValueError("El número de documento debe ser numérico")
        if len(supplier_id) not in [8, 11, 12]:
            raise ValueError("El número de documento debe ser de 8, 11 o 12 dígitos")
        if int(supplier_id) < 0:
            raise ValueError("El número de documento debe ser válido")
        if len(supplier_id) == 11 and supplier_id[0:2] not in ['10', '20']:
            raise ValueError("El número de documento debe ser válido")
        return supplier_id
    
class SupplierCategoryPost(SupplierCategory):
    pass

class SupplierCategoryPut(SupplierCategory):
    supplier_id: int

    @validator('supplier_id')
    def supplier_id_must_be_valid(cls, supplier_id):
        if supplier_id < 0:
            raise ValueError("El proveedor debe ser válido")
        return supplier_id