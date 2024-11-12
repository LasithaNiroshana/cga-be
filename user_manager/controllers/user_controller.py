from fastapi import APIRouter, HTTPException,status
from user_manager.services.user_service import UserService
from user_manager.database.schemas.user_schema import UserSchema, UserOutSchema
from user_manager.controllers.base_controller import BaseController
from user_manager.models.user_model import UserLoginModel, TokenResponseModel, UserResponseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
from user_manager.database.db import db
import configparser
import os
import jwt
import bcrypt

user_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# config = configparser.ConfigParser()
# config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cfg")
# config.read(config_path)s

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.cfg')
config.read(config_path)

SECRET_KEY = config["JWT"].get("SECRET_KEY")
ALGORITHM = config["JWT"].get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config["JWT"]["ACCESS_TOKEN_EXPIRE_MINUTES"])


class UserController(BaseController):

    @staticmethod
    async def register_user(user_data: dict):
        current_time = datetime.now()
        user_data["created_at"] = current_time
        user_data["updated_at"] = current_time

        # Hash the password using bcrypt
        hashed_password = UserService.hash_password(user_data["password"])
        user_data["password"] = hashed_password

        # Create the user in MongoDB
        try:
            user = db["users"].insert_one(user_data)
            created_user = db["users"].find_one({"_id": user.inserted_id})

            # Return the serialized user
            return BaseController.create_success(result=UserSchema(**created_user))
        except Exception as e:
            BaseController.ise(e)

    @staticmethod
    async def get_all_users():
        """Retrieve all users."""
        try:
            # Call service to fetch all users
            users = await UserService.fetch_all_users()
            if not users:
                return UserController.not_found("No users found.")
            return UserController.success(users)
        except Exception as e:
            UserController.ise(e)  # Handle internal server error

    """Hash password using bcrypt."""


class AuthController:
    @staticmethod
    def login_user(user: dict):
        email = user.get("email")
        password = user.get("password")
        try:
            user_data = db["users"].find_one({"email":email})
            if not user_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            user_service = UserService()
            if not user_service.verify_password(password, user_data["password"]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

            access_token = AuthController.create_access_token(data={"sub": email})
            user_details=AuthController.get_user_by_email(email)

            # response = UserResponseModel(
            #     access_token=access_token,
            #     token_type="bearer",
            #     user={
            #         "email": user["email"],
            #         "first_name": user.get("first_name",""),
            #         "last_name": user.get("last_name",""),
            #         "mobile": user.get("mobile",""),
            #     }
            # )
            response=user_details
            return response


        except Exception as e:
            print("Error occurred in login_user:", e)  # Logs any unexpected errors
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Login failed due to server error")

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed."
            ) from e

    @staticmethod
    def get_user_by_email(email: str):
        user = db.users.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        print("Fetched user document:", user)
        return user




