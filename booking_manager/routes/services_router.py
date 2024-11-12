from fastapi import APIRouter, Depends
from booking_manager.controllers.service_controller import ServicesController
from booking_manager.database.db import get_database
from pymongo.errors import ConnectionFailure
from booking_manager.models import service_model
from booking_manager.models.service_model import ServiceModel

services_router=APIRouter(
    prefix="/services",
    tags=["Services"]
)

@services_router.get("/get_all_services", response_model=list)
def get_all_services(db=Depends(get_database)):
    controller = ServicesController(db)
    return controller.get_all_services()

@services_router.get("/test_connection")
async def test_connection():
    try:
        # Try to ping the database to ensure the connection is active
        db = get_database()
        db.command("ping")  # This sends a ping to MongoDB to check connectivity
        return {"status": 1, "message": "Connected to MongoDB successfully."}
    except ConnectionFailure:
        return {"status": 0, "message": "Failed to connect to MongoDB."}

# @services_router.post("/add_service", response_model=ServiceModel)
# def get_all_services(db=Depends(get_database)):
#     controller = ServicesController(db)
#     return ServiceModel
