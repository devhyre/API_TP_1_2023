from pydantic import BaseModel, validator
from datetime import datetime

class Combo(BaseModel):
    name: str
    description: str
    path_image: str
    case_id: int
    quantity_case: int
    motherboard_id: int
    quantity_motherboard: int
    procesador_id: int
    quantity_procesador: int
    ram_id: int
    quantity_ram: int
    almacenamiento_id: int
    quantity_almacenamiento: int
    cooler_id: int = None
    quantity_cooler: int = None
    gpu_id: int = None
    quantity_gpu: int = None
    fan_id: int = None
    quantity_fan: int = None
    fuente_id: int = None
    quantity_fuente: int = None
    
class ComboPost(Combo):
    pass

class ComboPut(BaseModel):
    name: str
    description: str
    path_image: str