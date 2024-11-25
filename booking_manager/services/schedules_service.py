from booking_manager.database.db import get_database
from booking_manager.models.schedules_model import SchedulesModel
from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from bson import ObjectId


class SchedulesService:
    @staticmethod
    async def create_schedule(schedule_schema: SchedulesSchema) -> dict:
        try:
            schedule_dict = schedule_schema.dict(exclude_unset=True)

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
