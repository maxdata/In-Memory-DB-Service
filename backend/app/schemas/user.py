"""API schemas for users."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr, Field, BaseModel, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common attributes"""

    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(
        ..., min_length=1, max_length=100, description="User's full name"
    )
    is_active: bool = Field(default=True, description="Whether the user is active")


class UserIn(UserBase):
    """Schema for user input data."""

    password: str = Field(
        ..., min_length=8, max_length=100, description="User's password"
    )


class UserUpdate(BaseModel):
    """Schema for user update data."""

    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User's full name"
    )
    password: Optional[str] = Field(
        None, min_length=8, max_length=100, description="User's password"
    )
    is_active: Optional[bool] = Field(None, description="Whether the user is active")


class UserOut(UserBase):
    """Schema for user output data."""

    id: UUID = Field(..., description="Unique identifier of the user")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the user was last updated"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-03-22T00:00:00Z",
                "updated_at": "2024-03-22T00:00:00Z",
            }
        }
    )


class UsersOut(BaseModel):
    """Schema for listing multiple users."""

    data: List[UserOut] = Field(..., description="List of users")
    count: int = Field(..., description="Total number of users")


# Update exports
__all__ = ["UserBase", "UserIn", "UserUpdate", "UserOut", "UsersOut"]
