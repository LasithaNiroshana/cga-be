from fastapi import HTTPException
from booking_manager.services.schedules_service import SchedulesService
from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from booking_manager.controllers.base_controller import BaseController

class SchedulesController:

    @staticmethod
    async def create_schedule(schedules_schema: SchedulesSchema):
        """Create a new schedule for a service."""
        try:
            # Call the ScheduleService to create a schedule
            schedule_data = await SchedulesService.create_schedule(schedules_schema)

            # Return a success response using BaseController
            return BaseController.success(schedule_data, "Schedule created successfully.")

        except Exception as e:
            # Handle any exceptions using BaseController
            return BaseController.ise(e)

    # You can add more methods for schedule-related actions like update, delete, etc.

