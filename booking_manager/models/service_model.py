from bson import ObjectId
from pydantic import BaseModel
from booking_manager.database.db import get_database

db = get_database()
services_collection = db['services']

class ServiceModel:
    def __init__(self, service_id: str, name: str, description: str):
        self.service_id = service_id
        self.name = name
        self.description = description

    def model_dump(self):
        return {"service_id": self.service_id, "name": self.name, "description": self.description}

class AvailableTimeModel:
    collection = db['available_times']  # Collection for available times





