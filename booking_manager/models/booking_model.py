from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from bson.objectid import ObjectId

class PyObjectId(ObjectId):
    """MongoDB ObjectId custom type to integrate with Pydantic."""
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "minLength": 24, "maxLength": 24}

    @field_serializer
    def serialize_to_str(self, value: "PyObjectId") -> str:
        """Convert ObjectId to string when serializing."""
        return str(value)

class BookingCreateRequest(BaseModel):
    user_id: str
    service_id: str
    booking_type: str
    booking_time: str
    booking_date: str
    booking_source: str
    status: str
    created_by: str

    class Config:
        json_encoders = {
            "_id": str,
        }
        populate_by_name = True
        arbitrary_types_allowed = True
    

