from pydantic import BaseModel, validator
from datetime import datetime

class RepairsMaintenance(BaseModel):
    service_id: int
    type_id: int
    entry_date: datetime
    departure_date: datetime
    client_doc: str
    client_name: str
    client_email: str
    serial_number: str
    description: str
    note_diagnostic: str
    note_repair: str
    status_id: int
    discount: int
    price: float
    
class RepairsMaintenancePost(RepairsMaintenance):
    pass


class RepairsMaintenancePut(BaseModel):
    description: str
    note_diagnostic: str
    note_repair: str

class RepairsMaintenanceStatusPut(BaseModel):
    status_id: int