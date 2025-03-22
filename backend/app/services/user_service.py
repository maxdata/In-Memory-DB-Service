from datetime import datetime
from typing import Dict, List, Any, Optional
from uuid import UUID, uuid4

from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema
from app.db.base import InMemoryDB, RecordNotFoundError


class UserService:
    """Service layer for handling user-related business logic and database operations"""

    def __init__(self, db: InMemoryDB):
        self.db = db
        self.table_name = "users"

    async def create_user(self, user_data: UserCreateSchema) -> User:
        """Create a new user with business logic validation"""
        # Convert schema to model
        user_dict = user_data.model_dump()
        user_dict["id"] = uuid4()
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # Store in database
        stored_user = await self.db.create(self.table_name, str(user_dict["id"]), user_dict)
        
        # Convert back to model
        return User.model_validate(stored_user)

    async def get_user(self, user_id: UUID) -> User:
        """Get a user by ID with business logic handling"""
        try:
            user_dict = await self.db.read(self.table_name, str(user_id))
            return User.model_validate(user_dict)
        except RecordNotFoundError:
            raise ValueError(f"User with ID {user_id} not found")

    async def update_user(self, user_id: UUID, user_data: UserUpdateSchema) -> User:
        """Update a user's data with business logic validation"""
        # Get existing user
        existing_user = await self.get_user(user_id)
        
        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Store in database
        updated_user = await self.db.update(self.table_name, str(user_id), {
            **existing_user.model_dump(),
            **update_data
        })
        
        # Convert back to model
        return User.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user by ID"""
        return await self.db.delete(self.table_name, str(user_id))

    async def list_users(self) -> List[User]:
        """List all users with business logic handling"""
        users_dict = await self.db.list(self.table_name)
        return [User.model_validate(user) for user in users_dict] 