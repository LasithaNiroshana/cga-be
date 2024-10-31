from pydantic import BaseModel

class Service(BaseModel):
    id:str
    service_name:str
    availability:str
