from fastapi import APIRouter, status
from booking_manager.models.service_model import Service

services_router=APIRouter(
    prefix="/services",
    tags=["Services"]
)

@services_router.get('/get_service',status_code=status.HTTP_201_CREATED)
async def register_user(request: Service, service_controller: ServiceController = Depends(UserController)):
    return user_controller.sign_up(model=request)
