from pydantic import BaseModel, validator
from datetime import datetime

class Combo(BaseModel):
    name: str
    description: str
    path_image: str
    case_id: int
    case_quantity: int
    motherboard_id: int
    motherboard_quantity: int
    procesador_id: int
    procesador_quantity: int
    ram_id: int
    ram_quantity: int
    almacenamiento_id: int
    almacenamiento_quantity: int
    cooler_id: int = None
    cooler_quantity: int = None
    gpu_id: int = None
    gpu_quantity: int = None
    fan_id: int = None
    fan_quantity: int = None
    fuente_id: int = None
    fuente_quantity: int = None
    worker_id: int
    
class ComboPost(Combo):
    pass

class ComboPut(BaseModel):
    name: str
    description: str
    path_image: str