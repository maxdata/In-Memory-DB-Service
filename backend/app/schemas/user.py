"""API schemas for users."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import EmailStr, Field, BaseModel


class UserBase(BaseModel):
    """Base user schema with common attributes"""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., description="User's full name")
    is_active: bool = Field(default=True, description="Whether the user is active")


class UserIn(UserBase):
    """Schema for user input data."""
    password: str = Field(..., min_length=8, description="User's password")


class UserOut(UserBase):
    """Schema for user output data."""
    id: UUID = Field(..., description="Unique identifier of the user")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(..., description="Timestamp when the user was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-03-22T00:00:00Z",
                "updated_at": "2024-03-22T00:00:00Z"
            }
        }


class UsersOut(BaseModel):
    """Schema for listing multiple users."""
    data: List[UserOut] = Field(..., description="List of users")
    count: int = Field(..., description="Total number of users")
