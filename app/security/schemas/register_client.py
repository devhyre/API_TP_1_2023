from pydantic import BaseModel

class RegisterClient(BaseModel):
    tipoDocumento: str
    numeroDocumento: str
    nombreCompleto: str
    correoElectronico: str
    contrasena: str
    estadoUsuario: str
    repetirContrasena: str

    class Config:
        orm_mode = True