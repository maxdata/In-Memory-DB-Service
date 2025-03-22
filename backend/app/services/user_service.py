from typing import List
from uuid import UUID, uuid4
from datetime import datetime

from app.db.base import InMemoryDB, RecordNotFoundError, DatabaseError
from app.schemas.user import UserIn, UserOut, UserUpdate
from .base_service import BaseService


class UserService(BaseService):
    """Service layer for handling user-related operations"""

    def __init__(self, db: InMemoryDB):
        super().__init__(db, "users")

    async def create_user(self, user_data: UserIn) -> UserOut:
        """Create a new user"""
        # Create user dict with generated fields
        user_dict = user_data.model_dump()
        user_dict["id"] = str(
            uuid4()
        )  # Store ID as string since that's what DB expects
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        user_dict["hashed_password"] = (
            f"hashed_{user_dict['password']}"  # TODO: Implement proper hashing
        )
        del user_dict["password"]

        # Store in DB
        record_id = await self.db.create_record(self.table_name, user_dict)
        stored_user = await self.db.get_record(self.table_name, record_id)
        if not stored_user:
            raise DatabaseError("Failed to retrieve created user")
        return UserOut(**stored_user)

    async def get_user(self, user_id: UUID) -> UserOut:
        """Get a user by ID"""
        user = await self.db.get_record(self.table_name, user_id)
        if not user:
            raise RecordNotFoundError(f"User with ID {user_id} not found")
        return UserOut(**user)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserOut:
        """Update a user's data"""
        # Get current user data
        current_user = await self.db.get_record(self.table_name, user_id)
        if not current_user:
            raise RecordNotFoundError(f"User with ID {user_id} not found")

        # Update with new data
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        if "password" in update_data:
            update_data["hashed_password"] = (
                f"hashed_{update_data['password']}"  # TODO: Implement proper hashing
            )
            del update_data["password"]

        user_dict = {**current_user, **update_data, "updated_at": datetime.utcnow()}
        success = await self.db.update_record(self.table_name, user_id, user_dict)
        if not success:
            raise DatabaseError(f"Failed to update user with ID {user_id}")

        # Fetch and return updated user
        updated_user = await self.db.get_record(self.table_name, user_id)
        if not updated_user:
            raise DatabaseError(f"Failed to retrieve updated user with ID {user_id}")
        return UserOut(**updated_user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        success = await self.db.delete_record(self.table_name, user_id)
        if not success:
            raise RecordNotFoundError(f"User with ID {user_id} not found")
        return True

    async def list_users(self, bulk_mode: bool = False) -> List[UserOut]:
        """
        List all users.

        Args:
            bulk_mode: If True, uses optimized bulk retrieval (Note: base DB doesn't support this yet)
        """
        users = await self.db.list_records(self.table_name)
        return [UserOut.model_validate(user) for user in users]
