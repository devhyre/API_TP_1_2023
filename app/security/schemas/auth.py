import re
from pydantic import BaseModel, validator

class UserLogin(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_must_be_valid(cls, username):
        if not username.isalnum():
            raise ValueError("El nombre de usuario debe ser alfanumérico")
        if len(username) < 4 or len(username) > 20:
            raise ValueError("El nombre de usuario debe tener entre 4 y 20 caracteres")
        return username
    
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
    
class UserLoginResponse(BaseModel):
    username: str
    token: str
    token_type: str
    message: str
