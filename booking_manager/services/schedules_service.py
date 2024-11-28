from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.db import get_database
from booking_manager.models.schedules_model import SchedulesModel
from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from bson import ObjectId


class SchedulesService:
    @staticmethod
    async def create_schedule(schedule_schema: SchedulesSchema) -> dict:
        """Create schedule"""
        try:
            schedule_dict = schedule_schema.model_dump(exclude_unset=True)

            # Check if `id` is present, if not MongoDB will generate it automatically
            if 'id' not in schedule_dict:
                schedule_dict['id'] = str(ObjectId())  # Manually set the ID

            schedule_collection = get_database()["schedules"]
            result = schedule_collection.insert_one(schedule_dict)

            created_schedule = schedule_collection.find_one({"_id": result.inserted_id})

            # Convert ObjectId to string
            created_schedule["id"] = str(created_schedule["_id"])
            created_schedule.pop("_id", None)

            return created_schedule

        except Exception as e:
            raise Exception(f"An error occurred while creating the schedule: {str(e)}")

    @staticmethod
    async def get_schedule_by_service_id(service_id:str) ->list:
        """Get schedule by service id"""
        try:
            schedules_collection = get_database()['schedules']
            cursor = schedules_collection.find({"service_id":service_id})
            schedules = list(cursor)

            if not schedules:
                return BaseController.not_found()

            for override in schedules:
                override["id"] = str(override.pop("_id", None))

            return schedules

        except Exception as e:
            raise Exception(f"Error retrieving schedule overrides for service ID {service_id}: {str(e)}")

