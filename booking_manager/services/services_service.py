from sys import exception
from pymongo import DESCENDING
from pymongo.errors import PyMongoError
from booking_manager.models.service_model import ServiceModel
from booking_manager.database.db import get_database,db
from booking_manager.database.schemas.services_schema import ServiceSchema
from bson import ObjectId
from datetime import datetime

class ServicesService:

    @staticmethod
    async def create_service(service_schema: ServiceSchema) -> dict:
        """Create a new service"""
        try:
            # Convert the Pydantic model to a dictionary
            service_dict = service_schema.model_dump(exclude_unset=True, by_alias=True)

            if 'schedules' not in service_dict:
                service_dict['schedules'] = []

            # Insert into the database
            service_dict['created_at'] = datetime.now()
            service_collection = get_database()["services"]
            result =  service_collection.insert_one(service_dict)

            # Fetch the created service and ensure serialization
            created_service = service_collection.find_one({"_id": result.inserted_id})
            if created_service:
                created_service["_id"] = str(created_service["_id"])

            return created_service

        except Exception as e:
            raise Exception(f"An error occurred while creating the service: {str(e)}")


    @staticmethod
    async def get_services() -> list:
        """Get all the services"""
        try:
            services_collection=get_database()["services"]

            services_cursor=services_collection.find().sort("created_at",-1)
            # print("Raw cursor result:", list(services_collection.find()))

            services = list(services_cursor)
            for service in services:
                if "_id" in service:
                    service["id"] = str(service["_id"])  # Convert ObjectId to string
                    del service["_id"]

            # print("Processed services:", services)
            return services

        except PyMongoError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    async def delete_service(service_id:str)->dict:
        """Delete a service"""
        try:
            if not ObjectId.is_valid(service_id):
                raise ValueError(f"Invalid service ID: {service_id}")

            object_id = ObjectId(service_id)

            service_collection=get_database()["services"]
            result = service_collection.delete_one({"_id": object_id})

            if result.deleted_count == 0:
                raise Exception(f"No service found with ID: {service_id}")

            return {"message": f"Service with ID {service_id} successfully deleted."}

        except ValueError as ve:
            raise Exception(f"Invalid ObjectId format: {service_id}") from ve
        except PyMongoError as pe:
            raise Exception(f"Error interacting with the database: {str(pe)}") from pe
        except Exception as e:
            raise Exception(f"An error occurred while deleting the service: {str(e)}")


    # @staticmethod
    # async def edit_service(service_id:str,updated_service:ServiceSchema):
    #     """Edit a  service"""
    #     try:
    #         object_id=ObjectId(service_id)
    #         updated_data=updated_service.model_dump(exclude_none=True)
    #         updated_data["updated_at"] = datetime.now()
    #
    #         service_collection = get_database()["services"]
    #         updated_result=service_collection.update_one( {"_id": object_id}, {"$set": updated_data})
    #
    #         if updated_result.matched_count == 0:
    #             raise ValueError (f"No service found with id:{service_id}")
    #
    #         updated_service_data = service_collection.find_one({"_id":object_id})
    #         return updated_service_data
    #
    #     except Exception as e:
    #         raise Exception(f"An error occurred while updating the service:{e}")








