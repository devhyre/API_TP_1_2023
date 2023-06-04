from pydantic import BaseModel
from datetime import datetime

class Client(BaseModel):
    user_id: str
    created_at: datetime
    last_connection: datetime
    
class ClientPost(Client):
    pass

class ClientPut(Client):
    last_connection: datetime