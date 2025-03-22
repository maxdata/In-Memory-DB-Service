from collections import defaultdict
from typing import Dict, List, Any, Optional
from asyncio import Lock


class DatabaseError(Exception):
    """Base exception for database operations"""
    pass


class DuplicateRecordError(DatabaseError):
    """Raised when attempting to create a duplicate record"""
    pass


class RecordNotFoundError(DatabaseError):
    """Raised when a record is not found"""
    pass


class InMemoryDB:
    """
    InMemoryDB implements the Singleton pattern with table-level locking for concurrent operations.

    Key Features:
    1. Singleton Pattern: Ensures only one database instance exists application-wide
    2. Table-Level Locking: Each table has its own asyncio.Lock for write operations
    3. Concurrent Access:
       - Write operations (create, update, delete) are protected by table-specific locks
       - Read operations don't acquire locks, allowing concurrent reads
       - Operations on different tables can proceed concurrently
    4. Thread Safety: Asyncio locks ensure thread-safe access to table data
    """

    # Class variable to hold the single instance
    _instance: Optional["InMemoryDB"] = None
    _initialized: bool = False

    def __new__(cls) -> "InMemoryDB":
        """Controls instance creation to implement the Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initializes the database instance only once."""
        if not self._initialized:
            # Main storage for table data: {table_name: {record_id: record_data}}
            self._storage: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
            # Table-level locks: {table_name: asyncio.Lock()}
            self._locks: Dict[str, Lock] = defaultdict(Lock)
            self._initialized = True

    async def create(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record with table-level locking."""
        async with self._locks[table]:
            if record_id in self._storage[table]:
                raise DuplicateRecordError(f"Record {record_id} already exists in {table}")
            self._storage[table][record_id] = data.copy()
            return data

    async def read(self, table: str, record_id: str) -> Dict[str, Any]:
        """Read a record without acquiring a lock."""
        if record := self._storage[table].get(record_id):
            return record.copy()
        raise RecordNotFoundError(f"Record {record_id} not found in {table}")

    async def update(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record with table-level locking."""
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            self._storage[table][record_id].update(data)
            return self._storage[table][record_id].copy()

    async def delete(self, table: str, record_id: str) -> bool:
        """Delete a record with table-level locking."""
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            del self._storage[table][record_id]
            return True

    async def list(self, table: str) -> List[Dict[str, Any]]:
        """List all records in a table."""
        return [record.copy() for record in self._storage[table].values()]

    async def clear_table(self, table: str) -> None:
        """Clear all records from a table."""
        async with self._locks[table]:
            self._storage[table].clear()
