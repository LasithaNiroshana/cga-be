from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import date

class PyObjectId(ObjectId):
    """MongoDB ObjectId custom type to integrate with Pydantic."""
    pass

class ScheduleOverrideModel(BaseModel):
    id: PyObjectId = None
    service_id: PyObjectId  # Foreign key relation to the ServiceModel
    date: date  # The specific date for the override
    start_time: str  # Example: '09:00 AM - 10:00 AM'
    end_time:str
    full_day:bool
    is_included: bool  # True for includes, False for excludes

    class Config:
        json_encoders = {
            PyObjectId: str,
            ObjectId: str,
        }
