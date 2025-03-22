"""Simple database models."""

from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Basic user model"""

    id: str = str(uuid4())
    email: EmailStr
    full_name: str
    password: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
