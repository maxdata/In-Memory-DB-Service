"""Simple database models for orders."""

from datetime import datetime
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Order(BaseModel):
    """Basic order model."""

    id: str = str(uuid4())
    user_id: str
    amount: float = Field(gt=0)  # amount must be greater than 0
    description: str
    status: str = "pending"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class UserOrder(BaseModel):
    """Basic user order model."""

    user_id: str
    user_email: EmailStr  # validates email format
    user_full_name: Optional[str] = None
    order_id: str
    amount: float = Field(gt=0)  # amount must be greater than 0
    description: str
    status: str = "pending"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
