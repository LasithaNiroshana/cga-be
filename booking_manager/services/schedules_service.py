from datetime import datetime, timedelta, date
from itertools import filterfalse
from typing import List

from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.db import get_database
from booking_manager.models.schedules_model import SchedulesModel
from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from bson import ObjectId

from booking_manager.services.schedule_override_service import ScheduleOverrideService


class SchedulesService:
    # @staticmethod
    # async def create_schedule(schedule_schema: SchedulesSchema) -> dict:
    #     """Create schedule"""
    #     try:
    #         schedule_dict = schedule_schema.model_dump(exclude_unset=True)
    #
    #         # Check if `id` is present, if not MongoDB will generate it automatically
    #         if 'id' not in schedule_dict:
    #             schedule_dict['id'] = str(ObjectId())  # Manually set the ID
    #
    #         schedule_collection = get_database()["schedules"]
    #         result = schedule_collection.insert_one(schedule_dict)
    #
    #         created_schedule = schedule_collection.find_one({"_id": result.inserted_id})
    #
    #         # Convert ObjectId to string
    #         created_schedule["id"] = str(created_schedule["_id"])
    #         created_schedule.pop("_id", None)
    #
    #         return created_schedule
    #
    #     except Exception as e:
    #         raise Exception(f"An error occurred while creating the schedule: {str(e)}")

    @staticmethod
    async def create_schedule(schedule_schema:SchedulesSchema) -> dict:
        try:
            schedule_dict = schedule_schema.model_dump(exclude_unset=True)\


            start_time = datetime.strptime(schedule_dict["start_time"], "%H:%M")
            end_time = datetime.strptime(schedule_dict["end_time"], "%H:%M")
            minimum_slot_minutes = schedule_dict["minimum_slot"]

            if start_time >= end_time:
                raise ValueError("start_time must be earlier than end_time")

            if minimum_slot_minutes <= 0:
                raise ValueError("minimum_slot must be greater than 0")

            available_slots = []
            current_slot = start_time

            while current_slot + timedelta(minutes=minimum_slot_minutes) <= end_time:
                next_slot = current_slot + timedelta(minutes=minimum_slot_minutes)
                available_slots.append(f"{current_slot.strftime('%H:%M')}-{next_slot.strftime('%H:%M')}")
                current_slot = next_slot

            schedule_dict["available_slots"] = available_slots

            # if 'id' not in schedule_dict:
            #     schedule_dict['id'] = str(ObjectId())

            if "date" in schedule_dict:
                if isinstance(schedule_dict["date"], (datetime, date)):
                    schedule_dict["date"] = schedule_dict["date"].strftime("%Y-%m-%d")
                elif isinstance(schedule_dict["date"], str):
                    try:
                        schedule_dict["date"] = datetime.fromisoformat(schedule_dict["date"]).strftime("%Y-%m-%d")
                    except ValueError:
                        raise ValueError("Invalid date format. Use 'yyyy-mm-dd'.")

            schedule_collection = get_database()["schedules"]
            # print(schedule_dict)
            result = schedule_collection.insert_one(schedule_dict)

            created_schedule = schedule_collection.find_one({"_id": result.inserted_id})

            created_schedule["id"] = str(created_schedule["_id"])
            created_schedule.pop("_id", None)

            return created_schedule

        except ValueError as ve:
            raise Exception(f"Validation error: {str(ve)}")
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

    # @staticmethod
    # async def get_available_schedules(service_id:str) -> list:
    #     try:
    #         if not ObjectId.is_valid(service_id):
    #             return BaseController.bad_request("Invalid service_id provided.")
    #
    #         # print("line 1 is running")
    #         schedules_collection = get_database()["schedules"]
    #         schedule_overrides_collection = get_database()["schedule_overrides"]
    #         # schedules_data = list(schedules_collection)
    #
    #         today = datetime.now()
    #         end_of_week = today + timedelta(days=(6 - today.weekday()))
    #
    #         schedules = list(
    #             schedules_collection.find({"service_id": ObjectId(service_id),
    #                                        "date": {"$gte": today, "$lte": end_of_week},
    #                                        })
    #         )
    #
    #         schedule_overrides = list(
    #             schedule_overrides_collection.find(
    #                 {"service_id": ObjectId(service_id), "is_included": True,
    #                  "date": {"$gte": today, "$lte": end_of_week},
    #                  })
    #         )
    #
    #         valid_schedules = []
    #         for schedule in schedules:
    #             override = next(
    #                 (
    #                     o
    #                     for o in schedule_overrides
    #                     if o["date"].date() == schedule["date"].date()
    #                 ),
    #                 None
    #             )
    #
    #             if not override or override.get("full_day",None):
    #                 valid_schedules.append(schedule)
    #             elif override.get("full_day") is False:
    #                 valid_schedules.append(schedule)
    #
    #
    #         for override in schedule_overrides:
    #             if override.get("full_day",False) and not any(
    #                 s["date"].date() == override["date"].date() for s in schedules
    #             ):
    #                 valid_schedules.append(override)
    #
    #         return valid_schedules
    #
    #     except Exception as e:
    #         raise Exception(f"Error retrieving schedule overrides for service ID {service_id}: {str(e)}")

    @staticmethod
    async def get_available_schedules(service_id:str):
        try:
            schedules = await SchedulesService.get_schedule_by_service_id(service_id)
            overrides = await ScheduleOverrideService.get_schedule_override_by_service_id(service_id)

            if not schedules:
                return BaseController.not_found()

            valid_schedules = []
            print("Line 2")

            for schedule in valid_schedules:
                print("line 3")
                has_override = False

                for override in overrides:
                    if (
                        override["date"].date() == schedule["date"].date()
                        and override["full_day"]
                        and override["is_included"]
                    ):
                        # Add schedules with full_day=true and is_included=true
                        valid_schedules.append(schedule)
                        has_override = True
                        break
                    elif (
                        override["date"].date() == schedule["date"].date()
                        and not override["full_day"]
                        and override["is_included"]
                    ):
                        # Modify schedule for overrides with full_day=false
                        schedule["start_time"] = override["start_time"]
                        schedule["end_time"] = override["end_time"]
                        valid_schedules.append(schedule)
                        has_override = True
                        break

                if not has_override:
                    return BaseController.not_found().body

            return BaseController.success(valid_schedules)

        except Exception as e:
            return BaseController.ise(e)





