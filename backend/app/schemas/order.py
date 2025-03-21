from datetime import datetime
from uuid import UUID
from pydantic import Field
from .base import BaseSchema

class OrderCreate(BaseSchema):
    user_id: UUID
    product_name: str
    quantity: int
    total_price: float
    order_date: datetime = Field(default_factory=datetime.utcnow)

class OrderResponse(OrderCreate):
    pass

class OrderUpdate(BaseSchema):
    product_name: str | None = None
    quantity: int | None = None
    total_price: float | None = None 