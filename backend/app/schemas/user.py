from pydantic import EmailStr
from .base import BaseSchema

class UserCreate(BaseSchema):
    email: EmailStr
    full_name: str
    age: int

class UserResponse(UserCreate):
    pass

class UserUpdate(BaseSchema):
    email: EmailStr | None = None
    full_name: str | None = None
    age: int | None = None 