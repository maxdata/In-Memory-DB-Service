"""
FastAPI dependency module that provides access to services through dependency injection.

This module demonstrates proper layering by providing service-level dependencies
rather than direct database access.
"""

from typing import Annotated

from fastapi import Depends

from app.db.base import InMemoryDB
from app.services.user_service import UserService
from app.services.order_service import OrderService


def get_memory_db() -> InMemoryDB:
    """
    Internal dependency to get the in-memory database instance.
    This should only be used by service-level dependencies.
    """
    return InMemoryDB()


def get_user_service() -> UserService:
    """
    Dependency to get the UserService instance.
    Uses the singleton database instance internally.
    """
    return UserService(get_memory_db())


def get_order_service() -> OrderService:
    """
    Dependency to get the OrderService instance.
    Uses the singleton database instance internally.
    """
    return OrderService(get_memory_db())


# Type-annotated dependencies for FastAPI
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
