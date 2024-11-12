from fastapi import APIRouter
from user_manager.routes.user_router import user_router

user_manager_router=APIRouter()

user_manager_router.include_router(user_router)