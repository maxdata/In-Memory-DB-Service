"""Base service class for database operations."""

from uuid import UUID
from typing import Dict, List, Optional, Any
from app.db.base import InMemoryDB


class BaseService:
    """Base service class for database operations"""

    def __init__(self, db: InMemoryDB, table_name: str):
        """Initialize service with database instance and table name"""
        self.db = db
        self.table_name = table_name

    async def create(self, data: Dict[str, Any]) -> UUID:
        """Create a new record in the database"""
        return await self.db.create_record(self.table_name, data)

    async def get(self, record_id: UUID) -> Optional[Dict[str, Any]]:
        """Get a record by ID"""
        record = await self.db.get_record(self.table_name, record_id)
        if record is not None:
            record = record.copy()
            record["id"] = str(record_id)
        return record

    async def update(self, record_id: UUID, data: Dict[str, Any]) -> bool:
        """Update a record by ID"""
        return await self.db.update_record(self.table_name, record_id, data)

    async def delete(self, record_id: UUID) -> bool:
        """Delete a record by ID"""
        return await self.db.delete_record(self.table_name, record_id)

    async def list(self) -> List[Dict[str, Any]]:
        """List all records in the table"""
        records = await self.db.list_records(self.table_name)
        for record in records:
            record["id"] = str(record["id"]) if "id" in record else None
        return records

    async def exists(self, record_id: UUID) -> bool:
        """Check if a record exists by ID"""
        return await self.db.record_exists(self.table_name, record_id)

    async def clear_table(self) -> None:
        """Clear all records from the table"""
        await self.db.clear_table(self.table_name)
