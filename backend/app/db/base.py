from collections import defaultdict
from typing import Any, Dict, List, Optional
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
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._locks: Dict[str, Lock] = defaultdict(Lock)

    async def create(self, table: str, record_id: str, data: dict) -> dict:
        async with self._locks[table]:
            if record_id in self._storage[table]:
                raise DuplicateRecordError(f"Record {record_id} already exists in {table}")
            self._storage[table][record_id] = data
            return data

    async def read(self, table: str, record_id: str) -> Optional[dict]:
        if record := self._storage[table].get(record_id):
            return record
        raise RecordNotFoundError(f"Record {record_id} not found in {table}")

    async def update(self, table: str, record_id: str, data: dict) -> dict:
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            self._storage[table][record_id].update(data)
            return self._storage[table][record_id]

    async def delete(self, table: str, record_id: str) -> bool:
        async with self._locks[table]:
            if record_id not in self._storage[table]:
                raise RecordNotFoundError(f"Record {record_id} not found in {table}")
            del self._storage[table][record_id]
            return True

    async def list(self, table: str) -> List[dict]:
        return list(self._storage[table].values())

    async def join(self, table1: str, table2: str, key: str) -> List[dict]:
        results = []
        for record1 in self._storage[table1].values():
            key_value = record1.get(key)
            if key_value is not None:
                for record2 in self._storage[table2].values():
                    if record2.get(key) == key_value:
                        results.append({**record1, **record2})
        return results

    def clear_table(self, table: str) -> None:
        self._storage[table].clear() 