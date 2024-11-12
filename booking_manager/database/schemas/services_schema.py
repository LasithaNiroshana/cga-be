from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from bson import ObjectId
from uuid import uuid4
from datetime import date, time

# class TimeSlot(BaseModel):
#     start: time
#     end: time

class AvailableTimeSchema(BaseModel):
    id: Optional[str] = None  # To handle ObjectId serialization
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_mongo(cls, data):
        data['id'] = str(data['_id'])  # Convert ObjectId to string
        return cls(**data)

    # @field_validator("service_id")
    # def validate_objectid(cls, v):
    #     if not ObjectId.is_valid(v):
    #         raise ValueError("Invalid ObjectId")
    #     return str(v)


class ServiceSchema(BaseModel):
        service_id: str
        name: str
        description: str
        available_times: List[AvailableTimeSchema]

class ServicesResponse(BaseModel):
    services: List[ServiceSchema]

