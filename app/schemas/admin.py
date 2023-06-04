from pydantic import BaseModel, validator
from datetime import datetime

class Admin(BaseModel):
    user_id: str
    created_at: datetime
    last_connection: datetime
    role_id: int
    level: int

    @validator('level')
    def level_must_be_valid(cls, level):
        if level not in [0, 1, 2, 3, 4]:
            raise ValueError("El nivel de acceso debe ser válido")
        return level
    
class AdminPost(Admin):
    pass

class AdminPut(Admin):
    last_connection: datetime