"""Data models for the in-memory database service."""

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field, validator

# Add index for better performance
# hashmap for user_id
# Use primary key for better performance

# Order Models
class OrderBase(BaseModel):
    """Base model for order data."""

    product_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the ordered product"
    )
    quantity: int = Field(..., gt=0, description="Quantity of the product ordered")
    total_price: float = Field(..., gt=0, description="Total price of the order")
    status: str = Field("pending", description="Status of the order")

    @validator("status")
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


class OrderCreate(OrderBase):
    """Model for creating a new order."""

    user_id: UUID4 = Field(..., description="ID of the user placing the order")


class Order(OrderBase):
    """Model for an order in the database."""

    id: UUID4 = Field(
        default_factory=uuid4, description="Unique identifier for the order"
    )
    user_id: UUID4 = Field(..., description="ID of the user who placed the order")
    # make index for user_id as foreign key
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the order was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the order was last updated"
    )

    class Config:
        """Pydantic model configuration."""

        json_encoders = {UUID4: str, datetime: lambda v: v.isoformat()}


class OrderPublic(OrderBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime


class OrdersPublic(BaseModel):
    data: list[OrderPublic]
    count: int


# Joined User-Order Model
class UserOrder(BaseModel):
    user_id: UUID4
    user_email: EmailStr
    user_full_name: str | None
    order_id: UUID4
    product_name: str
    quantity: int
    price: float
    order_created_at: datetime


class UserOrdersPublic(BaseModel):
    data: list[UserOrder]
    count: int


# Generic message
class Message(BaseModel):
    message: str


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
User.update_forward_refs()
