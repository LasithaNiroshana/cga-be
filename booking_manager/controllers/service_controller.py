from fastapi import HTTPException

from booking_manager.controllers.base_controller import BaseController
from booking_manager.services.services_service import ServicesService
from booking_manager.database.schemas.services_schema import ServiceSchema

class ServicesController:

    @staticmethod
    async def create_service(service:ServiceSchema):
        try:
            service_data = await ServicesService.create_service(service)

            return BaseController.success(service_data,"Service created successfully.")

        except Exception as e:
            BaseController.ise(e)


