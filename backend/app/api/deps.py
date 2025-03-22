"""
FastAPI dependency module that provides access to the singleton database instance.

This module demonstrates how the singleton pattern ensures consistent database access
across all API endpoints through FastAPI's dependency injection system.
"""

from typing import Annotated

from fastapi import Depends

from app.db.base import InMemoryDB


def get_memory_db() -> InMemoryDB:
    """
    Dependency to get the in-memory database instance.

    Due to InMemoryDB's singleton pattern:
    1. This function can be called many times by different endpoints
    2. Each call to InMemoryDB() returns the same instance
    3. No matter how many times FastAPI injects this dependency, it's always the same database

    This ensures we're using the same database instance across all requests.
    """
    # Returns the singleton instance - InMemoryDB() will always return the same instance
    # due to the singleton pattern implemented in the InMemoryDB class
    return InMemoryDB()


# Type-annotated dependency for FastAPI
# When this type is used in endpoint parameters, FastAPI will call get_memory_db()
# The singleton pattern ensures it's always the same database instance
MemoryDBDep = Annotated[InMemoryDB, Depends(get_memory_db)]
