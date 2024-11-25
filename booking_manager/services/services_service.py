from sys import exception

from booking_manager.models.service_model import ServiceModel
from booking_manager.database.db import get_database
from booking_manager.database.schemas.services_schema import ServiceSchema
from bson import ObjectId

class ServicesService:
    @staticmethod
    async def create_service(service_schema: ServiceSchema) -> dict:
        try:
            # Convert the Pydantic model to a dictionary
            service_dict = service_schema.model_dump(exclude_unset=True, by_alias=True)

            if 'schedules' not in service_dict:
                service_dict['schedules'] = []

            # Insert into the database
            service_collection = get_database()["services"]
            result =  service_collection.insert_one(service_dict)

            # Fetch the created service and ensure serialization
            created_service = service_collection.find_one({"_id": result.inserted_id})
            if created_service:
                created_service["_id"] = str(created_service["_id"])

            return created_service

        except Exception as e:
            raise Exception(f"An error occurred while creating the service: {str(e)}")



