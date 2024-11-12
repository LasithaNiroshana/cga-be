from datetime import datetime
from pydantic import EmailStr, BaseModel
from bson import ObjectId
from typing import Optional

class UserModel:
    def __init__(self, id: str, email: EmailStr, first_name: str, last_name: str, mobile: str, status: str, user_role: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.status = status
        self.user_role = user_role
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_mongo(data: dict):
        """Convert MongoDB document to UserModel instance."""
        return UserModel(
            id=str(data["_id"]),  # Convert ObjectId to string for JSON compatibility
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            mobile=data["mobile"],
            status=data["status"],
            user_role=data["user_role"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

    # @staticmethod
    # def to_mongo(user_data):
    #     """Convert UserModel instance to MongoDB document."""
    #     return {
    #         "email": user_data.email,
    #         "first_name": user_data.first_name,
    #         "last_name": user_data.last_name,
    #         "mobile": user_data.mobile,
    #         "password": user_data.password,
    #         "status": user_data.status,
    #         "user_role": user_data.user_role,
    #         "created_at": datetime.utcnow(),
    #         "updated_at": datetime.utcnow()
    #     }

    # def to_dict(self):
    #     """Convert UserModel instance to dictionary format."""
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "mobile": self.mobile,
    #         "status": self.status,
    #         "user_role": self.user_role,
    #         "created_at": self.created_at,
    #         "updated_at": self.updated_at
    #     }

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class UserResponseModel(BaseModel):
    email: str = None
    first_name: str  = None
    last_name: str  = None
    mobile: str  = None
    password:str  = None

class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str

class UserView(BaseModel):
    id: Optional[str]
    email: EmailStr
    first_name: str
    last_name: str
    mobile: str
    user_role: str
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]
