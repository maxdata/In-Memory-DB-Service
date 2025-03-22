"""API schemas for orders."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator

from .base import BaseSchema


class OrderBase(BaseSchema):
    """Base order schema with common attributes"""

    amount: float = Field(gt=0, description="Total amount of the order")
    description: str = Field(..., description="Description of the order")
    status: str = Field(default="pending", description="Status of the order")


class OrderIn(OrderBase):
    """Schema for order input data."""

    user_id: UUID = Field(..., description="ID of the user placing the order")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate order status."""
        allowed_statuses = {
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
            "completed",
        }
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v


class OrderUpdate(BaseSchema):
    """Schema for order update data with optional fields."""

    amount: Optional[float] = Field(None, gt=0, description="Total amount of the order")
    description: Optional[str] = Field(None, description="Description of the order")
    status: Optional[str] = Field(None, description="Status of the order")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate order status if provided."""
        if v is None:
            return v

        allowed_statuses = {
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
            "completed",
        }
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v


class OrderOut(OrderBase):
    """Schema for order output data."""

    id: UUID = Field(..., description="Unique identifier of the order")
    user_id: UUID = Field(..., description="ID of the user who placed the order")
    created_at: datetime = Field(
        ..., description="Timestamp when the order was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the order was last updated"
    )


class OrdersOut(BaseSchema):
    """Schema for listing multiple orders."""

    data: List[OrderOut] = Field(..., description="List of orders")
    count: int = Field(..., description="Total number of orders")
