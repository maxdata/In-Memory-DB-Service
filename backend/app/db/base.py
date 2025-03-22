from collections import defaultdict
from typing import Any, Dict, List, Optional, TypeVar, Union
from asyncio import Lock
from uuid import uuid4, UUID

from app.models.user import User
from app.models.order import Order


class DatabaseError(Exception):
    """Base exception for database operations"""

    pass


class DuplicateRecordError(DatabaseError):
    """Raised when attempting to create a duplicate record"""

    pass


class RecordNotFoundError(DatabaseError):
    """Raised when a record is not found"""

    pass


T = TypeVar("T")


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

    Locking Strategy:
    - Each table has a dedicated lock in self._locks[table_name]
    - Write operations acquire the table's lock using 'async with self._locks[table]'
    - Read operations proceed without locks for better performance
    - Locks are automatically released after write operations complete
    """

    # Class variable to hold the single instance
    _instance: Optional["InMemoryDB"] = None
    _initialized: bool = False

    def __new__(cls) -> "InMemoryDB":
        """
        Controls instance creation to implement the Singleton pattern.

        This method is called before __init__ when creating a new instance.
        If _instance doesn't exist, creates it and marks it as uninitialized.
        If _instance exists, returns the existing instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the database instance only once.

        Initializes two key components:
        1. _storage: Dictionary of dictionaries to store table data
        2. _locks: Dictionary of asyncio.Lock objects for table-level locking

        The _initialized flag ensures initialization happens only once for the singleton.
        """
        if not self._initialized:
            # Main storage for table data: {table_name: {record_id: record_data}}
            self._storage: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
            # Table-level locks: {table_name: asyncio.Lock()}
            self._locks: Dict[str, Lock] = defaultdict(Lock)
            self._initialized = True

    async def create(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record with table-level locking.

        Acquires the table's lock before writing to prevent concurrent modifications
        to the same table. The lock is automatically released after the operation
        completes or if an error occurs.

        Args:
            table: Name of the table
            record_id: Unique identifier for the record
            data: Record data to store

        Returns:
            dict: The created record data

        Raises:
            DuplicateRecordError: If record_id already exists in the table
        """
        async with self._locks[table]:  # Acquire table lock for write operation
            if record_id in self._storage[table]:
                raise DuplicateRecordError(
                    f"Record {record_id} already exists in {table}"
                )
            self._storage[table][record_id] = data
            return data

    async def read(self, table: str, record_id: str) -> Dict[str, Any]:
        """
        Read a record without acquiring a lock.

        Read operations don't require locks as Python's dict operations are atomic
        and we prioritize read performance. Multiple reads can occur concurrently.

        Args:
            table: Name of the table
            record_id: Unique identifier for the record

        Returns:
            Dict[str, Any]: The record data if found

        Raises:
            RecordNotFoundError: If record_id doesn't exist in the table
        """
        if record := self._storage[table].get(record_id):
            return record
        raise RecordNotFoundError(f"Record {record_id} not found in {table}")

    async def update(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a record with table-level locking.

        Acquires the table's lock before updating to prevent concurrent modifications
        to the same table. The lock is automatically released after the operation
        completes or if an error occurs.

        Args:
            table: Name of the table
            record_id: Unique identifier for the record
            data: New record data to update

        Returns:
            dict: The updated record data

        Raises:
            RecordNotFoundError: If record_id doesn't exist in the table
        """
        async with self._locks[table]:  # Acquire table lock for write operation
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            self._storage[table][record_id].update(data)
            return self._storage[table][record_id]

    async def delete(self, table: str, record_id: str) -> bool:
        """
        Delete a record with table-level locking.

        Acquires the table's lock before deleting to prevent concurrent modifications
        to the same table. The lock is automatically released after the operation
        completes or if an error occurs.

        Args:
            table: Name of the table
            record_id: Unique identifier for the record

        Returns:
            bool: True if deletion was successful

        Raises:
            RecordNotFoundError: If record_id doesn't exist in the table
        """
        async with self._locks[table]:  # Acquire table lock for write operation
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            del self._storage[table][record_id]
            return True

    async def list(self, table: str) -> List[Dict[str, Any]]:
        return list(self._storage[table].values())

    async def join(self, table1: str, table2: str, key: str) -> List[Dict[str, Any]]:
        results = []
        for record1 in self._storage[table1].values():
            key_value = record1.get(key)
            if key_value is not None:
                for record2 in self._storage[table2].values():
                    if record2.get(key) == key_value:
                        results.append({**record1, **record2})
        return results

    async def clear_table(self, table: str) -> None:
        self._storage[table].clear()

    # User-specific methods
    async def add_user(self, user_data: User) -> Dict[str, Any]:
        """Add a new user to the database."""
        user_dict = user_data.model_dump()
        user_id = str(user_dict.get("id", uuid4()))
        return await self.create("users", user_id, user_dict)

    async def get_user(self, user_id: UUID) -> Dict[str, Any]:
        """Get a user by ID."""
        return await self.read("users", str(user_id))

    async def update_user(self, user_id: UUID, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user's data."""
        update_data = user_data.copy()
        update_data["id"] = str(user_id)  # Preserve the user's ID
        return await self.update("users", str(user_id), update_data)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user by ID."""
        return await self.delete("users", str(user_id))

    async def list_users(self) -> List[Dict[str, Any]]:
        """List all users."""
        return await self.list("users")

    # Order-specific methods
    async def add_order(self, order_data: Order) -> Dict[str, Any]:
        """Add a new order to the database."""
        order_dict = order_data.model_dump()
        order_id = str(order_dict.get("id", uuid4()))
        return await self.create("orders", order_id, order_dict)

    async def get_order(self, order_id: UUID) -> Dict[str, Any]:
        """Get an order by ID."""
        return await self.read("orders", str(order_id))

    async def update_order(self, order_id: UUID, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an order's data."""
        update_data = order_data.copy()
        update_data["id"] = str(order_id)  # Preserve the order's ID
        return await self.update("orders", str(order_id), update_data)

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order by ID."""
        return await self.delete("orders", str(order_id))

    async def list_orders(self) -> List[Dict[str, Any]]:
        """List all orders."""
        return await self.list("orders")

    async def get_user_orders(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get all orders for a specific user."""
        orders = await self.list_orders()
        return [order for order in orders if order.get("user_id") == str(user_id)]
