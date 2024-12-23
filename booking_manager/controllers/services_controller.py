from bson import ObjectId
from fastapi import HTTPException

from booking_manager.controllers.base_controller import BaseController
from booking_manager.services.services_service import ServicesService
from booking_manager.database.schemas.services_schema import ServiceSchema

class ServicesController:

    @staticmethod
    async def create_service(service:ServiceSchema):
        """Handle creating a new service"""
        try:
            service_data = await ServicesService.create_service(service)

            return BaseController.success(service_data,"Service created successfully.")

        except Exception as e:
            BaseController.ise(e)

    @staticmethod
    async def get_all_services():
        """Handle retrieving services"""
        try:
            services = await ServicesService.get_services()
            return BaseController.success(services,"Successfully retrieved services")

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while fetching services: {str(e)}"
            )

    @staticmethod
    async def delete_service(service_id:str):
        """Handle deleting a service"""
        try:
            result = await ServicesService.delete_service(service_id)
            return BaseController.success(result,result["message"])

        except Exception as e:
            if "No service found with ID" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            else:
                raise HTTPException(status_code=500, detail="An error occurred, please contact the administration.")

    @staticmethod
    async def edit_service(service_id:str,service:ServiceSchema):
        """Handle edit service"""
        try:
            if not ObjectId.is_valid(service_id):
                return BaseController.not_found()

            object_id=ObjectId(service_id)
            updated_service = await ServicesService.edit_service(object_id,service)

            if not updated_service:
                return BaseController.not_found()

            updated_service["_id"] = str(updated_service["_id"])

            return BaseController.success(updated_service, "Service updated successfully.")
        except Exception as e:
            raise Exception(f"An error occurred while editing the service: {str(e)}")


