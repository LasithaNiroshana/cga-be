from bson import ObjectId
from fastapi import HTTPException
from booking_manager.controllers.base_controller import BaseController
from booking_manager.services.services_service import ServicesService
from booking_manager.services.schedule_override_service import ScheduleOverrideService
from booking_manager.database.schemas.schedule_override_schema import ScheduleOverrideSchema

class ScheduleOverrideController:
    @staticmethod
    async def create_schedule_override(schedule_override_data:ScheduleOverrideSchema):
        """Handle creating schedule override"""
        try:
            schedule_override_data = await ScheduleOverrideService.create_schedule_override(schedule_override_data)
            return BaseController.success(schedule_override_data,"Schedule override created successfully.")

        except Exception as e:
            # Handle any exceptions using BaseController
            return BaseController.ise(e)

    @staticmethod
    async def get_all_schedule_overrides():
        try:
            schedule_override_list = await ScheduleOverrideService.get_all_schedule_overrides()
            if not schedule_override_list:
                return BaseController.not_found()

            return BaseController.success(schedule_override_list, "Schedule overrides retrieved successfully.")
        except Exception as e:
            return BaseController.ise(e)

    @staticmethod
    async def get_schedule_override_by_service_id(service_id:str):
        try:
            schedule_override_list = await ScheduleOverrideService.get_schedule_override_by_service_id(service_id)
            if not schedule_override_list:
                return BaseController.not_found()

            return BaseController.success(schedule_override_list, "Schedule overrides retrieved successfully.")
        except Exception as e:
            return BaseController.ise(e)
