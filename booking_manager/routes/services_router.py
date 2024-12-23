from fastapi import APIRouter, Depends

from booking_manager.controllers.base_controller import BaseController
from booking_manager.controllers.schedules_controller import SchedulesController
from booking_manager.controllers.services_controller import ServicesController
from booking_manager.controllers.schedule_override_controller import ScheduleOverrideController
# from booking_manager.controllers.service_controller import ServicesController
from booking_manager.database.db import get_database
from pymongo.errors import ConnectionFailure

from booking_manager.database.schemas.schedule_override_schema import ScheduleOverrideSchema
from booking_manager.database.schemas.schedules_schema import SchedulesSchema
from booking_manager.services.schedule_override_service import ScheduleOverrideService
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
    # try:
    #     # Call the service layer to create the service
    #     service_data = await ServicesService.create_service(service)
    #
    #     # Return a success response using BaseController
    #     return BaseController.success(service_data, "Service created successfully.")
    # except Exception as e:
    #     # Handle exceptions using BaseController
    #     BaseController.ise(e)
    return await ServicesController.create_service(service)

@services_router.post("/create_schedule", summary="Create a new schedule")
async def create_new_schedule(schedule:SchedulesSchema):
    """API to create a new schedule for a service."""
    return await SchedulesController.create_schedule(schedule)

@services_router.get("/get_all_services",summary="Get all services")
async def get_all_services():
    return await ServicesController.get_all_services()

@services_router.delete("/delete_service/{service_id}",summary="Delete a service")
async def delete_service(service_id:str):
    return await ServicesController.delete_service(service_id)

@services_router.put("/edit_service/{service_id}", summary="Edit an existing service")
async def edit_service(service_id:str,updated_service:ServiceSchema):
    return await ServicesController.edit_service(service_id,updated_service)

@services_router.post("/create_schedule_override", summary="Create new schedule override")
async def create_schedule_override(schedule_override:ScheduleOverrideSchema):
    return await ScheduleOverrideController.create_schedule_override(schedule_override)

# @services_router.post("/get_all_schedule_overrides", summary="Get all schedule overrides")
# async def get_all_schedule_overrides():
#     return await ScheduleOverrideController.get_all_schedule_overrides()

@services_router.get("/get_schedule_overrides_by_service_id/{service_id}", summary="Get schedule overrides by service id")
async def get_schedule_overrides_by_service_id(service_id:str):
    return await ScheduleOverrideService.get_schedule_override_by_service_id(service_id)

@services_router.get("/get_schedules_by_service_id{service_id}", summary = "Get schedules by service id")
async def get_schedules_by_service_id(service_id:str):
    return await SchedulesService.get_schedule_by_service_id(service_id)

@services_router.get("/get_available_schedules{service_id}", summary="Get available schedules")
async def get_available_schedules(service_id:str):
    return await SchedulesService.get_available_schedules(service_id)

