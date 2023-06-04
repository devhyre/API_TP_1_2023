from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ProfileResponse(BaseModel):
    id: int
    tipoDocumento: Optional[str]
    numeroDocumento: str
    nombreCompleto: str
    correoElectronico: str
    estadoUsuario: str
    fechaCreacion: datetime
    ultimoInicioSesion: datetime
    rol: Optional[str]
    nivelAcceso: Optional[int]

    class Config:
        orm_mode = True