from fastapi import APIRouter
from booking_manager.database.schemas.booking_schema import BookingSchema
from booking_manager.controllers.booking_controller import BookingController

booking_router=APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@booking_router.post("/create_booking", summary="Create a new booking")
async def create_booking(booking_request: BookingSchema):
    return await BookingController.create_booking(booking_request)



