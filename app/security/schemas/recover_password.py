import re
from pydantic import BaseModel, validator

class PasswordRecoveryRequest(BaseModel):
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
    
class PasswordRecoveryResponse(BaseModel):
    message: str

class PasswordResetRequest(BaseModel):
    token: str
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