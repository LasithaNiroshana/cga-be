from fastapi import APIRouter, HTTPException, Depends

from user_manager.database.schemas.user_schema import UserSchema
from user_manager.models.user_model import UserLoginModel, UserResponseModel
from user_manager.services.user_service import UserService
from user_manager.controllers.user_controller import UserController,AuthController
from user_manager.controllers.base_controller import BaseController

user_router = APIRouter(
prefix="/auth",
    tags=["User Authentication"]
)

# Create user API route
@user_router.post("/register_user", response_model=dict)
async def register_user(user_data: UserSchema):
    try:
        # Call the controller to register the user
        return await UserController.register_user(user_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all users API route
@user_router.get("/get_all_users", response_model=list)
async def get_all_users():
    try:
        # Call the controller to fetch all users
        return await UserController.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/login_user_new")
async def login_user(user: UserLoginModel):
    return AuthController.login_user(user.model_dump())