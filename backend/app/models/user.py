"""Data models for the in-memory database service."""

from datetime import datetime
from typing import Any, List
from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field, ConfigDict

from app.models.order import Order

__all__ = [
    "User",
    "UserCreate",
    "UserBase",
    "UserPublic",
    "UsersPublic",
    "UserOrder",
    "UserResponse",
]

# Add index for better performance
# hashmap for user_id
# Use primary key for better performance


# User Models
class UserBase(BaseModel):
    """Base model for user data."""

    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(
        ..., min_length=1, max_length=100, description="User's full name"
    )
    age: int | None = Field(None, ge=0, le=150, description="User's age")
    is_active: bool = Field(True, description="Whether the user is active")


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str = Field(..., min_length=8, description="User's password")


class User(UserBase):
    """Core user model with essential fields."""

    id: UUID4 = Field(
        default_factory=uuid4, description="Unique identifier for the user"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the user was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the user was last updated"
    )

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: UUID4


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


# Joined User-Order Model
class UserOrder(BaseModel):
    user_id: UUID4
    user_email: EmailStr
    user_full_name: str | None
    order_id: UUID4
    product_name: str
    quantity: int
    total_price: float  # Changed from price to total_price to match Order model
    order_created_at: datetime


# Response models
class UserResponse(User):
    """Response model for user data."""

    password: str | None = None  # Exclude password from responses


class OrderResponse(Order):
    """Response model for order data."""

    pass


class TableDump(BaseModel):
    """Model for table dump responses."""

    table_name: str
    records: list[dict[str, Any]]


class JoinResult(BaseModel):
    """Model for join operation results."""

    table1: str
    table2: str
    key: str
    records: list[dict[str, dict[str, Any]]]


# Update forward references
User.model_rebuild()
