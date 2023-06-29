import re
from typing import Optional
from pydantic import BaseModel, validator


class User(BaseModel):
    num_doc: str
    type_doc: int
    username: str
    full_name: Optional[str] = None
    email: str
    password: str
    is_active: bool

    """
    Tipo	Descripción Larga	                LO
    01	    LIBRETA ELECTORAL O DNI	            08
    04	    CARNET DE EXTRANJERIA	            12
    06	    REG. UNICO DE CONTRIBUYENTES	    11
    07	    PASAPORTE	                        12
    """

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
    
    @validator('type_doc')
    def type_doc_must_be_valid(cls, type_doc):
        if type_doc not in [1, 4, 6, 7]:
            raise ValueError("El tipo de documento debe ser válido")
        return type_doc
    
    @validator('username')
    def username_must_be_valid(cls, username):
        if not username.isalnum():
            raise ValueError("El nombre de usuario debe ser alfanumérico")
        if len(username) < 4 or len(username) > 20:
            raise ValueError("El nombre de usuario debe tener entre 4 y 20 caracteres")
        return username
    
    @validator('full_name')
    def full_name_must_be_valid(cls, full_name):
        if not re.match(r'^[a-zA-Z ]+$', full_name):
            raise ValueError("El nombre completo solo puede contener letras y espacios")
        if len(full_name) < 4 or len(full_name) > 100:
            raise ValueError("El nombre completo debe tener entre 4 y 100 caracteres")
        return full_name
    
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
    
    @validator('password')
    def password_must_be_valid(cls, password):
        if len(password) < 8 or len(password) > 20:
            raise ValueError("La contraseña debe tener entre 8 y 20 caracteres")
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula, una letra minúscula, un número y un caracter especial")
        if not re.match(r'^[\x20-\x7E]+$', password):
            raise ValueError("Caracteres no permitidos en la contraseña")
        if ' ' in password:
            raise ValueError("La contraseña no puede contener espacios")
        return password
    
class UserPost(BaseModel):
    num_doc: str
    type_doc: int
    username: str
    email: str
    password: str
    repeat_password: str

    @validator('repeat_password')
    def passwords_match(cls, repeat_password, values):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError("Las contraseñas no coinciden")
        return repeat_password
    
class UserPutEmail(BaseModel):
    email: str

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
    
class UserPutPassword(BaseModel):
    password: str
    repeat_password: str
    
    @validator('password')
    def password_must_be_valid(cls, password):
        if len(password) < 8 or len(password) > 20:
            raise ValueError("La contraseña debe tener entre 8 y 20 caracteres")
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula, una letra minúscula, un número y un caracter especial")
        if not re.match(r'^[\x20-\x7E]+$', password):
            raise ValueError("Caracteres no permitidos en la contraseña")
        if ' ' in password:
            raise ValueError("La contraseña no puede contener espacios")
        return password

    @validator('repeat_password')
    def passwords_match(cls, repeat_password, values):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError("Las contraseñas no coinciden")
        return repeat_password
