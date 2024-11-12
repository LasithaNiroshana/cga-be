from fastapi import FastAPI,APIRouter
from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.schemas.services_schema import ServiceSchema, AvailableTimeSchema
from booking_manager.models.service_model import AvailableTimeModel
from booking_manager.models.service_model import ServiceModel
from booking_manager.services.services_service import ServicesService
from booking_manager.database.schemas.services_schema import ServicesResponse

class ServicesController(BaseController):
    def __init__(self, db):
        self._services_service = ServicesService(db)

    def get_all_services(self):
        try:
            services = self._services_service.get_all_services()
            if not services:  # Check if services list is empty
                return self.success([], "No services currently available.")
            return self.success(services, "Services retrieved successfully.")
        except Exception as e:
            return self.ise(e)
