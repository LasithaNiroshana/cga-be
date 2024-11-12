from user_manager.database.db import db
from user_manager.models.user_model import UserModel
from passlib.context import CryptContext
from datetime import datetime
import bcrypt

# Initialize CryptContext with bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def create_user(user_data: dict):
        """Create a new user in the database."""
        # Hash the password
        hashed_password = pwd_context.hash(user_data["password"])

        # Prepare user data
        user = {
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "mobile": user_data["mobile"],
            "password": hashed_password,
            "status": "active",  # Default status
            "user_role": "user",  # Default role
            "created_at": user_data.get("created_at", None),
            "updated_at": user_data.get("updated_at", None)
        }

        # Insert the new user into the database
        result = db.users.insert_one(user)

        # Return the inserted user with the generated ID
        user["id"] = str(result.inserted_id)
        return user

    @staticmethod
    async def fetch_all_users():
        """Fetch all users from the database."""
        users_cursor = db.users.find()
        users = [user for user in users_cursor]

        # Convert ObjectId to string
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]  # Remove MongoDB's ObjectId field

        return users

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(plain_password:str, hashed_password:str)->bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

