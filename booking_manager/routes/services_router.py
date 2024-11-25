from fastapi import APIRouter, Depends

from booking_manager.controllers.base_controller import BaseController
from booking_manager.controllers.schedules_controller import SchedulesController
# from booking_manager.controllers.service_controller import ServicesController
from booking_manager.database.db import get_database
from pymongo.errors import ConnectionFailure

from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from booking_manager.services.schedules_service import SchedulesService
from booking_manager.services.services_service import ServicesService
from booking_manager.database.schemas.services_schema import ServiceSchema
from booking_manager.models import service_model
# from booking_manager.models.service_model import CreateServiceRequestModel,BookTimeSlotRequestModel, TimeSlotModel, ServiceCreateResponse, BookingResponse

services_router=APIRouter(
    prefix="/services",
    tags=["Services"]
)

# @services_router.get("/test_connection")
# async def test_connection():
#     try:
#         # Try to ping the database to ensure the connection is active
#         db = get_database()
#         db.command("ping")  # This sends a ping to MongoDB to check connectivity
#         return {"status": 1, "message": "Connected to MongoDB successfully."}
#     except ConnectionFailure:
#         return {"status": 0, "message": "Failed to connect to MongoDB."}

@services_router.post("/create_service",summary="Create a new service")
async def create_service(service: ServiceSchema):
    """API to create a service."""
    try:
        # Call the service layer to create the service
        service_data = await ServicesService.create_service(service)

        # Return a success response using BaseController
        return BaseController.success(service_data, "Service created successfully.")
    except Exception as e:
        # Handle exceptions using BaseController
        BaseController.ise(e)

@services_router.post("/create_schedule", summary="Create a new schedule")
async def create_new_schedule(schedule:SchedulesSchema):
    """API to create a new schedule for a service."""
    return await SchedulesController.create_schedule(schedule)

