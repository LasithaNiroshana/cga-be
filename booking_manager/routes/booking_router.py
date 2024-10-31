from fastapi import APIRouter
from booking_manager.models.booking_model import Booking

booking_router=APIRouter(
    prefix="/booking",
    tags=["Booking"]
)



