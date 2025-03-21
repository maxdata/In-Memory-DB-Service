from typing import Annotated

from fastapi import Depends

from backend.app.model.user import InMemoryDB, db


def get_memory_db() -> InMemoryDB:
    """
    Dependency to get the in-memory database instance.
    This ensures we're using the same database instance across all requests.
    """
    return db


# Type-annotated dependency for FastAPI
MemoryDBDep = Annotated[InMemoryDB, Depends(get_memory_db)]
