import re
from pydantic import BaseModel, validator

class Supplier(BaseModel):
    num_doc: str
    num_doc_representative: str
    email: str
    phone: str
    status: bool

    @validator('num_doc')
    def num_doc_must_be_valid(cls, num_doc):
        if not num_doc.isnumeric():
            raise ValueError("El número de documento debe ser numérico")
        if len(num_doc) not in [8, 11, 12]:
            raise ValueError("El número de documento debe ser de 8, 11 o 12 dígitos")
        if int(num_doc) < 0:
            raise ValueError("El número de documento debe ser válido")
        if len(num_doc) == 11 and num_doc[0:2] not in ['10', '20']:
            raise ValueError("El número de documento debe ser válido")
        return num_doc
    
    @validator('num_doc_representative')
    def num_doc_representative_must_be_valid(cls, num_doc_representative):
        if not num_doc_representative.isnumeric():
            raise ValueError("El número de documento del representante debe ser válido")
        return num_doc_representative
    
    @validator('email')
    def email_must_be_valid(cls, email):
        if len(email) < 10 or len(email) > 100:
            raise ValueError("El correo electrónico debe tener entre 10 y 100 caracteres")
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Correo electrónico inválido")
        if '..' in email:
            raise ValueError("El correo electrónico no puede contener puntos consecutivos")
        forbidden_chars = ['&', '=', "'", '+', ',', '<', '>']
        if any(char in email for char in forbidden_chars):
            raise ValueError("El correo electrónico no puede contener caracteres no permitidos")
        return email
    
    @validator('phone')
    def phone_must_be_valid(cls, phone):
        if not phone.isnumeric():
            raise ValueError("El número de teléfono debe ser válido")
        return phone
    
class SupplierPost(Supplier):
    pass

class SupplierPut(BaseModel):
    num_doc_representative: str
    email: str
    phone: str

    @validator('num_doc_representative')
    def num_doc_representative_must_be_valid(cls, num_doc_representative):
        if not num_doc_representative.isnumeric():
            raise ValueError("El número de documento del representante debe ser válido")
        return num_doc_representative
    
    @validator('email')
    def email_must_be_valid(cls, email):
        if len(email) < 10 or len(email) > 100:
            raise ValueError("El correo electrónico debe tener entre 10 y 100 caracteres")
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Correo electrónico inválido")
        if '..' in email:
            raise ValueError("El correo electrónico no puede contener puntos consecutivos")
        forbidden_chars = ['&', '=', "'", '+', ',', '<', '>']
        if any(char in email for char in forbidden_chars):
            raise ValueError("El correo electrónico no puede contener caracteres no permitidos")
        return email
    
    @validator('phone')
    def phone_must_be_valid(cls, phone):
        if not phone.isnumeric():
            raise ValueError("El número de teléfono debe ser válido")
        return phone
    
class SupplierPutStatus(BaseModel):
    status: bool