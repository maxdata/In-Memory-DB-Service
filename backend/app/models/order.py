"""Database models for orders."""

from datetime import datetime
from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator, ConfigDict

__all__ = [
    "Order",
    "UserOrder",
]

class Order(BaseModel):
    """Database model for orders."""

    id: UUID4 = Field(
        default_factory=uuid4, description="Unique identifier for the order"
    )
    user_id: UUID4 = Field(..., description="ID of the user who placed the order")
    product_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the ordered product"
    )
    quantity: int = Field(..., gt=0, description="Quantity of the product ordered")
    total_price: float = Field(..., gt=0, description="Total price of the order")
    status: str = Field("pending", description="Status of the order")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the order was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the order was last updated"
    )

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate order status."""
        allowed_statuses = {
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
        }
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID4: str,
            datetime: lambda v: v.isoformat(),
        },
    )


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
