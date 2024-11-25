from booking_manager.database.db import db
from bson.objectid import ObjectId
from datetime import datetime, time
from pydantic import BaseModel, Field, field_serializer
from typing import List, Optional, Any, Dict
from pymongo.errors import PyMongoError
from booking_manager.models.schedules_model import SchedulesModel


class PyObjectId(ObjectId):
    """MongoDB ObjectId custom type to integrate with Pydantic."""
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "minLength": 24, "maxLength": 24}

    @field_serializer
    def serialize_to_str(self, value: "PyObjectId") -> str:
        """Convert ObjectId to string when serializing."""
        return str(value)

class ServiceModel(BaseModel):
    # id: str = Field(..., alias="_id")
    name:str
    service_type:int #0=Fixed time slots 1=Variable time slots
    description: Optional[str] = None  # Optional description of the service
    price:float
    schedules: List[SchedulesModel] = []

    class Config:
        json_encoders = {
            "_id": str,
        }
        populate_by_name = True
        arbitrary_types_allowed = True

class ServiceWithId(ServiceModel):
    id: PyObjectId = Field(..., alias="_id")



