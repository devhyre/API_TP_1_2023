from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ProfileResponse(BaseModel):
    id: int
    tipoDocumento: int
    numeroDocumento: str
    nombreCompleto: str
    correoElectronico: str
    estadoUsuario: str
    fechaCreacion: datetime
    ultimoInicioSesion: datetime
    rol: int | None
    nivelAcceso: int | None

    class Config:
        orm_mode = True