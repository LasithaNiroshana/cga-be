from fastapi import APIRouter
from booking_manager.routes import booking_router
from booking_manager.routes import services_router

booking_manager_router=APIRouter()

booking_manager_router.routes(booking_router)
booking_manager_router.routes(services_router)