from typing import List, Optional
from pydantic import EmailStr, Field
from .base import BaseSchema
from app.models.user import UserBase, User


class UserCreateSchema(UserBase):
    """Schema for creating a new user via API"""
    password: str = Field(..., min_length=8, description="User's password")


class UserResponseSchema(User):
    """Schema for user responses in API"""
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "age": 30,
                "is_active": True,
                "created_at": "2024-03-22T00:00:00Z",
                "updated_at": "2024-03-22T00:00:00Z"
            }
        }


class UserUpdateSchema(BaseSchema):
    """Schema for updating a user via API"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: Optional[bool] = None


class UsersListResponseSchema(BaseSchema):
    """Schema for listing multiple users in API response"""
    data: List[UserResponseSchema]
    count: int
