from bson import ObjectId
from pydantic import BaseModel, field_validator, ConfigDict, GetCoreSchemaHandler, Field, model_validator, \
    field_serializer
from datetime import date, datetime
from typing import Optional
from pydantic_core import core_schema


class ScheduleOverrideSchema(BaseModel):
    # id: Optional[PyObjectId] = Field(default_factory=lambda: PyObjectId(str(ObjectId())))
    service_id: str  # Foreign key relation to the Service collection
    date: date  # Specific date for the override
    start_time: str  # Example: '09:00 AM - 10:00 AM'
    end_time: str
    full_day: bool  # Indicates if the override spans the whole day
    is_included: bool  # True for includes, False for excludes
    # model_config = ConfigDict(arbitrary_types_allowed=True)

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

    @field_serializer("date")
    def serialize_date(self, value: date) -> datetime:
        """
        Convert date to datetime for MongoDB storage.
        """
        return datetime.combine(value, datetime.min.time())

    class Config:
        json_encoders = {
            ObjectId: str,  # Ensure ObjectId is converted to string in JSON
            datetime: lambda v: v.isoformat(),  # Convert datetime to ISO format
        }
        populate_by_name = True