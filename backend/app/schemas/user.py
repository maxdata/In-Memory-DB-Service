"""API schemas for users."""

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, Field
from .base import BaseSchema
from app.models.user import UserBase, User


class UserBase(BaseSchema):
    """Base schema for user data."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str | None = Field(None, description="User's full name")


class UserIn(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, description="User's password")


class UserOut(UserBase):
    """Schema for user output data."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserResponseSchema(UserOut):
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


class UserUpdateIn(BaseSchema):
    """Schema for updating a user."""
    email: EmailStr | None = Field(default=None, description="User's email address")
    full_name: str | None = Field(default=None, description="User's full name")
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: Optional[bool] = None


class UsersListResponseSchema(BaseSchema):
    """Schema for listing multiple users in API response"""
    data: List[UserResponseSchema]
    count: int
