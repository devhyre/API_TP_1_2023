from pydantic import BaseModel, validator
from datetime import datetime

class RepairsMaintenance(BaseModel):
    type_service_id: int
    serial_number_id: str
    created_at: datetime
    worker_id: int
    description: str
    note: str
    status_id: int
    discount: int
    total: float

    @validator('type_service_id')
    def type_service_id_must_be_valid(cls, type_service_id):
        if type_service_id < 0:
            raise ValueError("El tipo de servicio debe ser válido")
        return type_service_id
    
    @validator('serial_number_id')
    def serial_number_id_must_be_valid(cls, serial_number_id):
        if not serial_number_id.isalnum():
            raise ValueError("El número de serie solo puede contener caracteres alfanuméricos")
        return serial_number_id
    
    @validator('worker_id')
    def worker_id_must_be_valid(cls, worker_id):
        if worker_id < 0:
            raise ValueError("El trabajador debe ser válido")
        return worker_id
    
    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener menos de 255 caracteres")
        return description
    
    @validator('note')
    def note_must_be_valid(cls, note):
        if len(note) > 255:
            raise ValueError("La nota debe tener menos de 255 caracteres")
        return note
    
    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id
    
    @validator('total')
    def total_must_be_valid(cls, total):
        if total < 0:
            raise ValueError("El total debe ser válido")
        return total
    
class RepairsMaintenancePost(RepairsMaintenance):
    pass


class RepairsMaintenancePut(RepairsMaintenance):
    description: str
    note: str
    status_id: int
    discount: int

    @validator('description')
    def description_must_be_valid(cls, description):
        if len(description) > 255:
            raise ValueError("La descripción debe tener menos de 255 caracteres")
        return description
    
    @validator('note')
    def note_must_be_valid(cls, note):
        if len(note) > 255:
            raise ValueError("La nota debe tener menos de 255 caracteres")
        return note
    
    @validator('status_id')
    def status_id_must_be_valid(cls, status_id):
        if status_id < 0:
            raise ValueError("El estado debe ser válido")
        return status_id