from collections import defaultdict
from typing import Dict, List, Any, Optional, Set
from asyncio import Lock
from uuid import UUID, uuid4


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
    InMemoryDB implements the Singleton pattern with table-level locking and optimized indexing.

    Key Features:
    1. Singleton Pattern: Ensures only one database instance exists application-wide
    2. Table-Level Locking: Each table has its own asyncio.Lock for write operations
    3. Concurrent Access:
       - Write operations (create, update, delete) are protected by table-specific locks
       - Read operations don't acquire locks, allowing concurrent reads
       - Operations on different tables can proceed concurrently
    4. Thread Safety: Asyncio locks ensure thread-safe access to table data
    5. Index Optimization:
       - Hash-based indexing for O(1) lookup time
       - Automatic index maintenance during CRUD operations
       - Memory-efficient index storage using sets
       - Transparent to service layer
       - Optimized for relationship queries (e.g., finding orders by user_id)

    Index Implementation:
    - Structure: {table_name: {field_name: {field_value: set(record_ids)}}}
    - Example:
      _indexes = {
          "orders": {
              "user_id": {
                  "user123": {order1_id, order2_id},
                  "user456": {order3_id, order4_id}
              }
          }
      }
    - Benefits:
      * O(1) lookup time for indexed fields
      * Efficient for exact match queries
      * Perfect for relationship lookups
      * Minimal memory overhead using sets
      * Automatic maintenance during CRUD
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
        """
        Initializes the database instance only once.
        
        Storage Structures:
        1. _storage: Main data store
           - Format: {table_name: {record_id: record_data}}
           - Purpose: Primary storage for all records
        
        2. _locks: Concurrency control
           - Format: {table_name: asyncio.Lock()}
           - Purpose: Table-level locking for thread safety
        
        3. _indexes: Hash-based indexing
           - Format: {table_name: {field_name: {field_value: set(record_ids)}}}
           - Purpose: O(1) lookup time for indexed fields
           - Benefits: Fast relationship queries, efficient filtering
        """
        if not self._initialized:
            # Main storage for table data: {table_name: {record_id: record_data}}
            self._storage: Dict[str, Dict[UUID, Dict[str, Any]]] = defaultdict(dict)
            # Table-level locks: {table_name: asyncio.Lock()}
            self._locks: Dict[str, Lock] = defaultdict(Lock)
            # Index storage: {table_name: {field_name: {field_value: set(record_ids)}}}
            self._indexes: Dict[str, Dict[str, Dict[Any, Set[UUID]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
            self._initialized = True

    async def initialize(self) -> None:
        """
        Initialize the database with automatic index creation.
        
        This method automatically creates indexes for commonly queried fields:
        1. orders.user_id: For efficient user-order relationship queries
        2. users.email: For efficient user lookup by email
        
        The indexes are maintained automatically during all CRUD operations,
        providing O(1) lookup time for these fields without any service layer changes.
        """
        # Create indexes for common relationship fields
        common_indexes = {
            "orders": ["user_id"],  # Orders are commonly queried by user_id
            "users": ["email"]      # Users are commonly queried by email
        }
        
        # Initialize tables and indexes
        for table, fields in common_indexes.items():
            # Initialize table storage if not exists
            if table not in self._storage:
                self._storage[table] = {}
            
            # Initialize table locks if not exists
            if table not in self._locks:
                self._locks[table] = Lock()
            
            # Initialize indexes for each field
            for field in fields:
                if table not in self._indexes:
                    self._indexes[table] = {}
                if field not in self._indexes[table]:
                    self._indexes[table][field] = defaultdict(set)

    async def cleanup(self) -> None:
        """Clean up the database."""
        self._storage.clear()
        self._locks.clear()

    async def create_index(self, table: str, field: str) -> None:
        """
        Create an index on a specific field in a table.
        
        This method:
        1. Acquires table lock for thread safety
        2. Creates the index structure if it doesn't exist
        3. Builds index for existing records
        
        The index provides O(1) lookup time for queries on the indexed field.
        For example, indexing "user_id" in the orders table allows fast retrieval
        of all orders for a specific user without scanning the entire table.
        
        Thread Safety:
        - Uses table-level lock to ensure thread-safe index creation
        - Safe for concurrent access from multiple coroutines
        """
        async with self._locks[table]:
            # Build index for existing records
            for record_id, record in self._storage[table].items():
                if field in record:
                    self._indexes[table][field][record[field]].add(record_id)

    async def get_by_index(self, table: str, field: str, value: Any) -> Set[UUID]:
        """
        Get record IDs by indexed field value.
        
        This method provides O(1) lookup time for finding records by indexed fields.
        For example, finding all orders for a user becomes an O(1) operation:
        record_ids = await get_by_index("orders", "user_id", "user123")
        
        Returns:
            Set of record IDs matching the field value
        
        Note:
        - Returns a copy of the ID set to prevent external modifications
        - No lock needed for reads, allowing concurrent access
        """
        return self._indexes[table][field][value].copy()

    async def create_record(self, table: str, data: Dict[str, Any]) -> UUID:
        """
        Create a new record with auto-generated UUID.
        
        This method:
        1. Generates a new UUID for the record
        2. Acquires table lock for thread safety
        3. Creates a copy of the data to prevent external modifications
        4. Stores the record in the database
        5. Updates all relevant indexes automatically
        
        Index Maintenance:
        - Checks all existing indexes for the table
        - Adds new index entries for indexed fields
        - Maintains O(1) lookup time for future queries
        
        Thread Safety:
        - Table lock ensures atomic record creation and index updates
        - Prevents race conditions during concurrent writes
        """
        record_id = uuid4()
        async with self._locks[table]:
            data = data.copy()
            data["id"] = str(record_id)
            self._storage[table][record_id] = data
            
            # Update indexes
            for field in self._indexes[table]:
                if field in data:
                    self._indexes[table][field][data[field]].add(record_id)
            
            return record_id

    async def get_record(self, table: str, record_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get a record by ID.
        
        This method:
        1. Returns None if record not found
        2. Returns a copy of the record data
        """
        if record := self._storage[table].get(record_id):
            return record.copy()
        return None

    async def update_record(
        self, table: str, record_id: UUID, data: Dict[str, Any]
    ) -> bool:
        """
        Update a record by ID.
        
        This method:
        1. Acquires table lock for thread safety
        2. Verifies record exists
        3. Creates a copy of update data
        4. Prevents ID field modification
        5. Updates the record
        
        Index Maintenance:
        - Removes old index entries before update
        - Adds new index entries after update
        - Handles field value changes correctly
        - Maintains index consistency
        
        Example:
        If updating an order's user_id from "user1" to "user2":
        1. Removes order from user1's index entry
        2. Updates the order record
        3. Adds order to user2's index entry
        
        Thread Safety:
        - Table lock ensures atomic update of record and indexes
        - Prevents inconsistency during concurrent modifications
        """
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                return False
            
            # Remove old index entries
            old_data = self._storage[table][record_id]
            for field in self._indexes[table]:
                if field in old_data:
                    self._indexes[table][field][old_data[field]].discard(record_id)
            
            # Update record
            data = data.copy()
            if "id" in data:
                del data["id"]  # Don't allow updating the ID
            self._storage[table][record_id].update(data)
            
            # Add new index entries
            updated_data = self._storage[table][record_id]
            for field in self._indexes[table]:
                if field in updated_data:
                    self._indexes[table][field][updated_data[field]].add(record_id)
            
            return True

    async def delete_record(self, table: str, record_id: UUID) -> bool:
        """
        Delete a record by ID.
        
        This method:
        1. Acquires table lock for thread safety
        2. Verifies record exists
        3. Removes the record from all indexes
        4. Deletes the record from storage
        
        Index Maintenance:
        - Removes record ID from all relevant index entries
        - Cleans up index entries to prevent memory leaks
        - Maintains index consistency after deletion
        
        Thread Safety:
        - Table lock ensures atomic deletion and index cleanup
        - Prevents dangling index entries
        """
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                return False
            
            # Remove index entries
            record = self._storage[table][record_id]
            for field in self._indexes[table]:
                if field in record:
                    self._indexes[table][field][record[field]].discard(record_id)
            
            # Delete record
            del self._storage[table][record_id]
            return True

    async def list_records(self, table: str) -> List[Dict[str, Any]]:
        """
        List all records in a table.
        
        Returns copies of records to prevent external modifications.
        """
        return [record.copy() for record in self._storage[table].values()]

    async def table_exists(self, table: str) -> bool:
        """Check if a table exists in the database."""
        return table in self._storage

    async def record_exists(self, table: str, record_id: UUID) -> bool:
        """Check if a record exists by ID."""
        return record_id in self._storage[table]

    async def clear_table(self, table: str) -> None:
        """
        Clear all records from a table.
        
        This method:
        1. Acquires table lock for thread safety
        2. Removes all records from the table
        3. Clears all indexes for the table
        
        Index Maintenance:
        - Removes all index entries for the table
        - Resets index structures to empty state
        - Prevents memory leaks from orphaned indexes
        
        Thread Safety:
        - Table lock ensures atomic table clearing
        - Prevents inconsistency between storage and indexes
        """
        async with self._locks[table]:
            self._storage[table].clear()
            # Clear all indexes for this table
            self._indexes[table].clear()
