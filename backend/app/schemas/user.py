from pydantic import EmailStr, Field
from .base import BaseSchema


class UserCreate(BaseSchema):
    email: EmailStr
    full_name: str
    age: int = Field(ge=0, le=150, description="Age must be between 0 and 150")


class UserResponse(UserCreate):
    pass


class UserUpdate(BaseSchema):
    email: EmailStr | None = None
    full_name: str | None = None
    age: int | None = Field(
        default=None, ge=0, le=150, description="Age must be between 0 and 150"
    )
