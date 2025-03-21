"""
CRUD operations for the in-memory database service.
"""

from typing import Any, TypeVar
from uuid import UUID

from backend.app.db import db
from backend.app.model.user import Order, User, UserCreate

# Define a generic type for models
ModelT = TypeVar("ModelT", User, Order)

# In-memory storage using dictionaries
tables: dict[str, dict[str, dict[str, Any]]] = {"users": {}, "orders": {}}

def create_user(*, data: dict[str, Any] | UserCreate) -> User:
    """Create a new user in the in-memory database."""
    if isinstance(data, UserCreate):
        user_data = data.model_dump()
    else:
        user_data = data
    user = User(**user_data)
    db.add_record("users", str(user.id), user.model_dump())
    return user


def get_user(*, user_id: UUID) -> User | None:
    """Get a user by ID from the in-memory database."""
    result = db.get_record("users", str(user_id))
    return User(**result) if result else None


def update_user(*, user_id: UUID, data: dict[str, Any]) -> User | None:
    """Update a user in the in-memory database."""
    result = db.update_record("users", str(user_id), data)
    return User(**result) if result else None


def delete_user(*, user_id: UUID) -> bool:
    """Delete a user from the in-memory database."""
    return db.delete_record("users", str(user_id))


def list_users() -> list[User]:
    """List all users in the in-memory database."""
    return [User(**user_data) for user_data in db.dump_table("users")]

