from fastapi import HTTPException

from booking_manager.database.schemas.booking_schema import BookingSchema
from booking_manager.services.booking_service import BookingService
from booking_manager.controllers.base_controller import BaseController

class BookingController:

    @staticmethod
    async def create_booking(booking_request:BookingSchema):
        try:
            return await BookingService.create_booking(booking_request)
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            return BaseController.ise(e)
