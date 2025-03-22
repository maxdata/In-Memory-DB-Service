from uuid import UUID
from pydantic import Field, field_validator
from .base import BaseSchema


class OrderCreate(BaseSchema):
    user_id: UUID
    product_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the ordered product"
    )
    quantity: int = Field(..., gt=0, description="Quantity of the product ordered")
    total_price: float = Field(..., gt=0, description="Total price of the order")
    status: str = Field("pending", description="Status of the order")

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
            "completed",  # Added to match test data
        }
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v


class OrderResponse(OrderCreate):
    id: UUID


class OrderUpdate(BaseSchema):
    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Name of the ordered product",
    )
    quantity: int | None = Field(
        default=None, gt=0, description="Quantity of the product ordered"
    )
    total_price: float | None = Field(
        default=None, gt=0, description="Total price of the order"
    )
    status: str | None = Field(default=None, description="Status of the order")
