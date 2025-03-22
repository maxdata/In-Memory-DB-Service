from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from app.db.base import InMemoryDB, RecordNotFoundError
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserResponse


class UserService:
    """Service layer for handling user-related operations"""

    def __init__(self, db: InMemoryDB):
        self.db = db
        self.table_name = "users"

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Create user dict with generated fields
        user_dict = user_data.model_dump()
        user_dict["id"] = uuid4()
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        user_dict["hashed_password"] = f"hashed_{user_dict['password']}"  # TODO: Implement proper hashing
        del user_dict["password"]

        # Store in DB
        stored_user = await self.db.create(self.table_name, str(user_dict["id"]), user_dict)
        return UserResponse(**stored_user)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """Get a user by ID"""
        user = await self.db.read(self.table_name, str(user_id))
        return UserResponse(**user)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """Update a user's data"""
        # Get current user data
        current_user = await self.db.read(self.table_name, str(user_id))
        
        # Update with new data
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = f"hashed_{update_data['password']}"  # TODO: Implement proper hashing
            del update_data["password"]
        
        user_dict = {**current_user, **update_data, "updated_at": datetime.utcnow()}
        updated_user = await self.db.update(self.table_name, str(user_id), user_dict)
        return UserResponse(**updated_user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        return await self.db.delete(self.table_name, str(user_id))

    async def list_users(self) -> List[UserResponse]:
        """List all users"""
        users = await self.db.list(self.table_name)
        return [UserResponse(**user) for user in users] 