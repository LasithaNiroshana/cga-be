from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId
from uuid import uuid4
from datetime import date, time

class TimeSlot(BaseModel):
    start: time
    end: time

class AvailableTimeSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Unique identifier (can be UUID)
    service_id: ObjectId  # ID of the associated service as ObjectId
    date: date
    hours: List[TimeSlot]

class ServiceSchema:
    id:str
    service_name:str
    availability:bool
    available_times: List[AvailableTimeSchema]


