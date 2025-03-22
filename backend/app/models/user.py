"""Database models for users."""

from datetime import datetime
from uuid import uuid4
from typing import Optional, List
from pydantic import UUID4, BaseModel, EmailStr, Field, ConfigDict

__all__ = [
    "User",
    "UserOrder",
    "Order",
]


class User(BaseModel):
    """User model with core attributes"""
    id: UUID4
    email: EmailStr
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class Order(BaseModel):
    """Order model with core attributes"""
    id: UUID4
    user_id: UUID4
    amount: float
    description: str
    status: str
    created_at: datetime
    updated_at: datetime


# Joined User-Order Model
class UserOrder(BaseModel):
    """Database model for joined user-order data."""
    user_id: UUID4
    user_email: EmailStr
    user_full_name: str | None
    order_id: UUID4
    product_name: str
    quantity: int
    total_price: float
    order_created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID4: str,
            datetime: lambda v: v.isoformat(),
        },
    )
