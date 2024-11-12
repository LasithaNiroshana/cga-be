from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import Field

class UserSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    email: EmailStr
    first_name: str
    last_name: str
    mobile: str
    password: str
    status: Optional[str] = "active"  # Default to active
    user_role: Optional[str] = "user"  # Default to user
    # created_at: datetime
    # updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            id: lambda v: str(v) # Automatically convert ObjectId to string when serializing
        }

class UserOutSchema(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    mobile: str
    status: str
    user_role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
