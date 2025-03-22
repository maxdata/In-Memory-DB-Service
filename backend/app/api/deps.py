"""
FastAPI dependency module that provides access to services through dependency injection.

This module implements a hierarchical dependency injection system that follows these principles:
1. Singleton Pattern: Database instance is shared across the application (implemented in InMemoryDB)
2. Dependency Inversion: Services depend on abstractions, not concrete implementations
3. Service Layer Pattern: API routes interact with services, not directly with the database
4. Clean Architecture: Dependencies flow inward (API -> Services -> Database)

Example Usage:
    ```python
    @app.get("/users/{user_id}")
    async def get_user(
        user_id: UUID,
        user_service: UserServiceDep
    ) -> UserOut:
        return await user_service.get_user(user_id)
    ```
"""

from typing import Annotated
from fastapi import Depends
from app.db.base import InMemoryDB
from app.services.user_service import UserService
from app.services.order_service import OrderService


def get_memory_db() -> InMemoryDB:
    """
    Get the InMemoryDB instance.

    The singleton pattern is implemented in the InMemoryDB class itself,
    ensuring only one database instance exists throughout the application.

    Returns:
        InMemoryDB: The singleton database instance
    """
    return InMemoryDB()


def get_user_service() -> UserService:
    """
    Dependency provider for UserService instances.

    This factory function:
    1. Creates a new UserService instance for each request
    2. Injects the singleton database dependency
    3. Ensures proper service isolation
    4. Enables easier testing through dependency injection

    Returns:
        UserService: A new service instance with injected dependencies
    """
    return UserService(get_memory_db())


def get_order_service() -> OrderService:
    """
    Dependency provider for OrderService instances.

    This factory function:
    1. Creates a new UserService instance for each request
    2. Injects the singleton database dependency
    3. Ensures proper service isolation
    4. Enables easier testing through dependency injection

    Returns:
        OrderService: A new service instance with injected dependencies
    """
    return OrderService(get_memory_db())


# Type-annotated dependencies for FastAPI
# These provide type-safe dependency injection in route handlers
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
