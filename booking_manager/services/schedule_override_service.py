from datetime import datetime, timedelta, date

from bson import ObjectId

from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.schemas.schedule_override_schema import ScheduleOverrideSchema
from booking_manager.database.db import get_database

class ScheduleOverrideService:

    @staticmethod
    async def create_schedule_override(schedule_override_data: ScheduleOverrideSchema):
        """Handle creating schedule override and updating related schedule"""
        try:
            # Step 1: Add the override to the schedule_overrides collection
            schedule_override_collection = get_database()["schedule_overrides"]
            schedule_override_dict = schedule_override_data.model_dump(exclude_none=True)

            if isinstance(schedule_override_dict["date"], date):
                # schedule_override_dict["date"] = datetime.combine(schedule_override_dict["date"], datetime.min.time())
                # schedule_override_dict["date"] = datetime.strptime(schedule_override_dict["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                schedule_override_dict["date"] = schedule_override_dict["date"].strftime("%Y-%m-%d")

            # Insert the override into the schedule_overrides collection
            result = schedule_override_collection.insert_one(schedule_override_dict)

            # Retrieve the created schedule override
            created_schedule_override = schedule_override_collection.find_one({"_id": result.inserted_id})
            created_schedule_override["id"] = str(created_schedule_override["_id"])
            created_schedule_override.pop("_id", None)

            schedule_collection = get_database()["schedules"]

            date_as_string = schedule_override_dict["date"]
            date_as_datetime = datetime.strptime(date_as_string, "%Y-%m-%d")
            schedule = schedule_collection.find_one({
                "service_id": schedule_override_data.service_id,
                "$or": [
                    {"date": date_as_string},
                    {"date": date_as_datetime}
                ]
            })

            if not schedule:
                raise Exception("Schedule not found for the given service_id and date.")

            # Calculate the time range from start_time to end_time
            start_time = datetime.strptime(schedule_override_data.start_time, "%H:%M")
            end_time = datetime.strptime(schedule_override_data.end_time, "%H:%M")
            time_slot_duration = timedelta(minutes=schedule["minimum_slot"])

            # Create a list of time slots from start_time to end_time based on minimum_slot
            current_time = start_time
            new_slots = []
            while current_time < end_time:
                slot_end_time = (current_time + time_slot_duration).strftime("%H:%M")
                new_slots.append(f"{current_time.strftime('%H:%M')}-{slot_end_time}")
                current_time += time_slot_duration

            # Update available_slots based on is_included
            if schedule_override_data.is_included:
                schedule["available_slots"] = list(set(schedule["available_slots"] + new_slots))
            else:
                schedule["available_slots"] = [
                    slot for slot in schedule["available_slots"] if slot not in new_slots
                ]

            # Update the schedule in the database
            schedule_collection.update_one(
                {"_id": ObjectId(schedule["_id"])},
                {"$set": {"available_slots": schedule["available_slots"]}}
            )

            # Step 3: Return the created schedule override and success message
            return {
                "schedule_override": created_schedule_override,
                "message": "Schedule override applied successfully."
            }

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


