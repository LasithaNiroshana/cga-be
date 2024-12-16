from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date
from bson import ObjectId
from typing import Optional, List

class SchedulesSchema(BaseModel):
    # id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    service_id: str
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    minimum_slot:int
    # available_slots: List[str]  # List of time slots, e.g., ["10:00-11:00", "11:00-12:00"]
    available_slots: Optional[List[str]] = Field(default=None, exclude=True)
    booked_slots: Optional[List[str]] = []
    start_time: str  # Format as HH:MM
    end_time: str  # Format as HH:MM
    date: datetime  # A full datetime object, if needed

    # Validator for service_id field to check if it's a valid ObjectId format
    @field_validator('service_id')
    def validate_service_id(cls, value):
        """Ensure that service_id is a valid ObjectId string."""
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid service_id format")
        return value

    # Model-level validator to ensure that the schema is valid as a whole
    @model_validator(mode='before')
    def check_fields(cls, values):
        """Ensure service_id is valid and not empty."""
        service_id = values.get('service_id')
        if service_id and not ObjectId.is_valid(service_id):
            raise ValueError("Invalid service_id format")
        return values

    class Config:
        json_encoders = {
            ObjectId: str,  # Ensure ObjectId is converted to string in JSON
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),  # Convert datetime to ISO format
        }

