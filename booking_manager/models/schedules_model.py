from bson import ObjectId
from pydantic import BaseModel
from datetime import time
from typing import Optional
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import List, Optional, Any, Dict
from datetime import time

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="objectid")
        return json_schema

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return ObjectId(value)

class SchedulesModel(BaseModel):
    id: Optional[str] = None  # Optional for auto-generation
    service_id: PyObjectId  # Reference to the Service ID (ObjectId)
    # day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    start_time: time
    end_time: time
    date: str  # The specific date for the schedule (ISO format)

    class Config:
        json_encoders = {
            PyObjectId: str,  # Serialize PyObjectId to string
        }

    def to_dict(self):
        return self.model_dump(by_alias=True)
