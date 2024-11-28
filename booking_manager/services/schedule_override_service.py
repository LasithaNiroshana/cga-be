from bson import ObjectId

from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.schemas.schedule_override_schema import ScheduleOverrideSchema
from booking_manager.database.db import get_database

class ScheduleOverrideService:

    @staticmethod
    async def create_schedule_override(schedule_override_data: ScheduleOverrideSchema):
        """Create new schedule override"""
        try:
            schedule_override_dict = schedule_override_data.model_dump(exclude_none=True)
            if "id" not in schedule_override_dict:
                schedule_override_dict["id"] = str(ObjectId())

            schedule_override_collection = get_database()["schedule_overrides"]
            result = schedule_override_collection.insert_one(schedule_override_dict)

            created_schedule_override = schedule_override_collection.find_one({"_id": result.inserted_id})
            created_schedule_override["id"] = str(created_schedule_override["_id"])
            created_schedule_override.pop("_id", None)

            return created_schedule_override

        except Exception as e:
            raise Exception(f"An error occurred while creating the schedule override: {str(e)}")

    @staticmethod
    async def get_all_schedule_overrides() -> list:
        """Get all schedule overrides"""
        try:
            schedule_override_collection = get_database()["schedule_overrides"]
            cursor = schedule_override_collection.find()
            schedule_overrides = list(cursor)

            if not schedule_overrides:
                return BaseController.not_found()

            for override in schedule_overrides:
                override["id"] = str(override.pop("_id", None))

            return schedule_overrides

        except Exception as e:
            raise BaseController.ise(e)


    @staticmethod
    async def get_schedule_override_by_service_id(service_id:str) -> list:
        """Get schedule overrides by service id"""
        try:
            schedule_override_collection = get_database()["schedule_overrides"]
            cursor = schedule_override_collection.find({"service_id":service_id})
            schedule_overrides = list(cursor)

            if not schedule_overrides:
                return BaseController.not_found()

            for override in schedule_overrides:
                override["id"] = str(override.pop("_id", None))

            return schedule_overrides

        except Exception as e:
            # Handle database errors
            raise Exception(f"Error retrieving schedule overrides for service ID {service_id}: {str(e)}")


