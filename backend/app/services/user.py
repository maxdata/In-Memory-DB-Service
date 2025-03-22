"""
CRUD operations for the in-memory database service.
"""

from typing import Any, TypeVar, List, Optional
from uuid import UUID, uuid4

from app.db import db
from app.models.user import User, UserCreate, UserResponse
from app.db.base import InMemoryDB

T = TypeVar("T")


class UserService:
    """
    Service for managing user operations.
    """

    def __init__(self, db_instance: InMemoryDB = None):
        """
        Initialize the service with a database instance.
        """
        self.db = db_instance or db

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_data: User data to create

        Returns:
            UserResponse: Created user data
        """
        user_dict = user_data.model_dump()
        user_dict["id"] = uuid4()
        user = User(**user_dict)
        result = await self.db.add_user(user)
        return UserResponse(**result)

    async def get_user(self, user_id: UUID) -> Optional[UserResponse]:
        """
        Get a user by ID.

        Args:
            user_id: User ID to get

        Returns:
            Optional[UserResponse]: User data if found
        """
        try:
            result = await self.db.get_user(user_id)
            return UserResponse(**result)
        except Exception:
            return None

    async def update_user(self, user_id: UUID, user_data: dict) -> Optional[UserResponse]:
        """
        Update a user.

        Args:
            user_id: User ID to update
            user_data: User data to update

        Returns:
            Optional[UserResponse]: Updated user data
        """
        try:
            result = await self.db.update_user(user_id, user_data)
            return UserResponse(**result)
        except Exception:
            return None

    async def delete_user(self, user_id: UUID) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID to delete

        Returns:
            bool: True if deletion was successful
        """
        try:
            return await self.db.delete_user(user_id)
        except Exception:
            return False

    async def list_users(self) -> List[UserResponse]:
        """
        List all users.

        Returns:
            List[UserResponse]: List of users
        """
        try:
            results = await self.db.list_users()
            return [UserResponse(**user) for user in results]
        except Exception:
            return []


def create_user(*, data: dict[str, Any] | UserCreate) -> User:
    """Create a new user in the in-memory database."""
    if isinstance(data, UserCreate):
        user_data = data.model_dump()
    else:
        user_data = data
    user = User(**user_data)
    db.add_user(user)
    return user


def get_user(*, user_id: UUID) -> Optional[User]:
    """Get a user by ID from the in-memory database."""
    return db.get_user(user_id)


def update_user(*, user_id: UUID, data: dict[str, Any]) -> Optional[User]:
    """Update a user in the in-memory database."""
    return db.update_user(user_id, data)


def delete_user(*, user_id: UUID) -> bool:
    """Delete a user from the in-memory database."""
    return db.delete_user(user_id)


def list_users() -> list[User]:
    """List all users in the in-memory database."""
    return db.list_users()
