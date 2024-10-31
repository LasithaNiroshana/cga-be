from pydantic import BaseModel

class AvailableTimes(BaseModel):
    id:str
    service_name:str
    availability:str
