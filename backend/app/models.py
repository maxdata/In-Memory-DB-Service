"""Data models for the in-memory database service."""

from datetime import datetime
from uuid import uuid4
from typing import Any

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


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
    """Model for a user in the database."""

    id: UUID4 = Field(
        default_factory=uuid4, description="Unique identifier for the user"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the user was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the user was last updated"
    )
    orders: list["Order"] = Field(
        default_factory=list, description="Orders associated with this user"
    )

    class Config:
        """Pydantic model configuration."""

        json_encoders = {UUID4: str, datetime: lambda v: v.isoformat()}


class UserPublic(UserBase):
    id: UUID4


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


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


# In-Memory Database
class InMemoryDB:
    """In-memory database implementation."""

    def __init__(self) -> None:
        """Initialize empty database."""
        self.users: dict[UUID4, User] = {}
        self.orders: dict[UUID4, Order] = {}

    def add_user(self, user: UserCreate | User) -> User:
        """Add a user to the database."""
        if isinstance(user, UserCreate):
            user_dict = user.model_dump()
            user = User(**user_dict)
        self.users[user.id] = user
        return user

    def add_order(self, order: Order) -> Order:
        """Add an order to the database."""
        self.orders[order.id] = order
        return order

    def get_user(self, user_id: UUID4) -> User | None:
        """Get a user by ID."""
        return self.users.get(user_id)

    def get_order(self, order_id: UUID4) -> Order | None:
        """Get an order by ID."""
        return self.orders.get(order_id)

    def update_user(self, user_id: UUID4, user_data: dict[str, Any]) -> User | None:
        """Update a user's data."""
        if user := self.users.get(user_id):
            updated_data = user.model_dump()
            updated_data.update(user_data)
            updated_user = User(**updated_data)
            self.users[user_id] = updated_user
            return updated_user
        return None

    def update_order(self, order_id: UUID4, order_data: dict[str, Any]) -> Order | None:
        """Update an order's data."""
        if order := self.orders.get(order_id):
            updated_data = order.model_dump()
            updated_data.update(order_data)
            updated_order = Order(**updated_data)
            self.orders[order_id] = updated_order
            return updated_order
        return None

    def delete_user(self, user_id: UUID4) -> bool:
        """Delete a user and their associated orders."""
        if user_id in self.users:
            del self.users[user_id]
            # Delete associated orders
            self.orders = {k: v for k, v in self.orders.items() if v.user_id != user_id}
            return True
        return False

    def delete_order(self, order_id: UUID4) -> bool:
        """Delete an order."""
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False

    def list_users(self) -> list[User]:
        """List all users."""
        return list(self.users.values())

    def list_orders(self) -> list[Order]:
        """List all orders."""
        return list(self.orders.values())

    def join_user_orders(self) -> list[UserOrder]:
        """Join users and orders data."""
        joined_data = []
        for order in self.orders.values():
            if user := self.users.get(order.user_id):
                joined_data.append(
                    UserOrder(
                        user_id=user.id,
                        user_email=user.email,
                        user_full_name=user.full_name,
                        order_id=order.id,
                        product_name=order.product_name,
                        quantity=order.quantity,
                        price=order.total_price,
                        order_created_at=order.created_at,
                    )
                )
        return joined_data


# Initialize in-memory database
db = InMemoryDB()


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
