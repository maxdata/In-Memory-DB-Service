"""
CRUD operations for the in-memory database service.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union, cast
from uuid import UUID

from .models import Order, User, UserCreate

# Define a generic type for models
ModelT = TypeVar('ModelT', User, Order)

# In-memory storage using dictionaries
tables: Dict[str, Dict[str, Dict[str, Any]]] = {"users": {}, "orders": {}}


class InMemoryDB:
    """In-memory database implementation."""

    @staticmethod
    def add_record(table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a record to the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        if record_id in tables[table]:
            raise ValueError(f"Record with id {record_id} already exists in {table}")

        # Add creation timestamp
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = data["created_at"]

        tables[table][record_id] = data
        return data

    @staticmethod
    def get_record(table: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Get a record from the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        return tables[table].get(record_id)

    @staticmethod
    def update_record(table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record in the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        if record_id not in tables[table]:
            raise KeyError(f"Record {record_id} not found in table {table}")

        # Update the record while preserving created_at
        current_record = tables[table][record_id]
        updated_record = {**current_record, **data}
        updated_record["updated_at"] = datetime.utcnow().isoformat()

        tables[table][record_id] = updated_record
        return updated_record

    @staticmethod
    def delete_record(table: str, record_id: str) -> bool:
        """Delete a record from the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        if record_id not in tables[table]:
            return False

        # Handle cascading deletes for orders when deleting a user
        tables[table].pop(record_id)
        if table == "users":
            # Delete all orders for this user
            orders_to_delete = [
                order_id
                for order_id, order in tables["orders"].items()
                if order.get("user_id") == record_id
            ]
            for order_id in orders_to_delete:
                tables["orders"].pop(order_id)

        return True

    @staticmethod
    def join_tables(table1: str, table2: str, key: str) -> List[Dict[str, Dict[str, Any]]]:
        """Join two tables based on a common key."""
        if table1 not in tables or table2 not in tables:
            raise KeyError(f"One or both tables not found: {table1}, {table2}")

        if table1 == table2:
            raise ValueError("Cannot join table with itself")

        result = []
        for record1 in tables[table1].values():
            if key not in record1:
                continue
            key_value = record1[key]

            for record2 in tables[table2].values():
                if key in record2 and record2[key] == key_value:
                    joined_record = {table1: record1, table2: record2}
                    result.append(joined_record)

        return result

    @staticmethod
    def dump_table(table: str) -> List[Dict[str, Any]]:
        """Dump all contents of the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        return list(tables[table].values())

    @staticmethod
    def clear_table(table: str) -> None:
        """Clear all records from the specified table."""
        if table not in tables:
            raise KeyError(f"Table {table} does not exist")

        tables[table].clear()


# Create a single instance of the database
db = InMemoryDB()


def create_user(*, data: Union[Dict[str, Any], UserCreate]) -> User:
    """Create a new user in the in-memory database."""
    if isinstance(data, UserCreate):
        user_data = data.model_dump()
    else:
        user_data = data
    user = User(**user_data)
    db.add_record("users", str(user.id), user.model_dump())
    return user


def get_user(*, user_id: UUID) -> Optional[User]:
    """Get a user by ID from the in-memory database."""
    result = db.get_record("users", str(user_id))
    return User(**result) if result else None


def update_user(*, user_id: UUID, data: Dict[str, Any]) -> Optional[User]:
    """Update a user in the in-memory database."""
    result = db.update_record("users", str(user_id), data)
    return User(**result) if result else None


def delete_user(*, user_id: UUID) -> bool:
    """Delete a user from the in-memory database."""
    return db.delete_record("users", str(user_id))


def list_users() -> List[User]:
    """List all users in the in-memory database."""
    return [User(**user_data) for user_data in db.dump_table("users")]


def create_order(*, data: Dict[str, Any]) -> Order:
    """Create a new order in the in-memory database."""
    order = Order(**data)
    db.add_record("orders", str(order.id), order.model_dump())
    return order


def get_order(*, order_id: UUID) -> Optional[Order]:
    """Get an order by ID from the in-memory database."""
    result = db.get_record("orders", str(order_id))
    return Order(**result) if result else None


def update_order(*, order_id: UUID, data: Dict[str, Any]) -> Optional[Order]:
    """Update an order in the in-memory database."""
    result = db.update_record("orders", str(order_id), data)
    return Order(**result) if result else None


def delete_order(*, order_id: UUID) -> bool:
    """Delete an order from the in-memory database."""
    return db.delete_record("orders", str(order_id))


def list_orders() -> List[Order]:
    """List all orders in the in-memory database."""
    return [Order(**order_data) for order_data in db.dump_table("orders")]
