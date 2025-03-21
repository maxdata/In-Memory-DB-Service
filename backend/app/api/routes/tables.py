from typing import Any, Dict, List, Optional, Union, cast
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.deps import MemoryDBDep
from app.models import Message, Order, User, UserOrder

router = APIRouter(prefix="/api/v1", tags=["tables"])

# Map table names to their corresponding models
TABLE_MODELS = {"users": User, "orders": Order}


class GenericCreate(BaseModel):
    data: Dict[str, Any]


@router.post("/data/{table}", response_model=Dict[str, Any])
def add_record(*, db: MemoryDBDep, table: str, record: GenericCreate) -> Dict[str, Any]:
    """
    Add a record to the specified table.
    """
    if table not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")

    try:
        if table == "users":
            user = User(**record.data)
            result = db.add_user(user)
            return result.model_dump(exclude={"hashed_password"})
        else:  # table == "orders"
            order = Order(**record.data)
            result = db.add_order(order)
            return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/data/{table}/{record_id}", response_model=Dict[str, Any])
def update_record(
    *, db: MemoryDBDep, table: str, record_id: UUID, record: GenericCreate
) -> Dict[str, Any]:
    """
    Update a record in the specified table.
    """
    if table not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")

    try:
        if table == "users":
            result = db.update_user(record_id, record.data)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result.model_dump(exclude={"hashed_password"})
        else:  # table == "orders"
            result = db.update_order(record_id, record.data)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/data/{table}/{record_id}", response_model=Message)
def delete_record(*, db: MemoryDBDep, table: str, record_id: UUID) -> Message:
    """
    Delete a record from the specified table.
    """
    if table not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")

    success = False
    if table == "users":
        success = db.delete_user(record_id)
    elif table == "orders":
        success = db.delete_order(record_id)

    if not success:
        raise HTTPException(status_code=404, detail="Record not found")

    return Message(message=f"Record deleted successfully from {table}")


@router.get("/api/v1/tables/join", response_model=List[Dict[str, Dict[str, Any]]])
def join_tables(
    *, db: MemoryDBDep, table1: str, table2: str, key: str
) -> List[Dict[str, Dict[str, Any]]]:
    """
    Join two tables based on a common key.
    Currently supports joining users and orders tables.

    Args:
        db: Database dependency
        table1: First table name
        table2: Second table name
        key: Key to join on (e.g., 'user_id')

    Returns:
        List of joined records
    """
    if table1 not in TABLE_MODELS or table2 not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail="One or both tables not found")

    # Currently only supports users-orders join with user_id key
    if {table1, table2} == {"users", "orders"} and key == "user_id":
        joined_data = db.join_user_orders()
        return [
            {
                "user": {
                    "id": str(item.user_id),
                    "email": item.user_email,
                    "full_name": item.user_full_name,
                },
                "order": {
                    "id": str(item.order_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "created_at": item.order_created_at.isoformat(),
                },
            }
            for item in joined_data
        ]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Currently only supports joining users and orders tables on user_id key, got tables: {table1}, {table2} with key: {key}",
        )


@router.get("/data/{table}/dump", response_model=Dict[str, Any])
def dump_table(*, db: MemoryDBDep, table: str) -> Dict[str, Any]:
    """
    Dump all contents of the specified table.
    """
    if table not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")

    if table == "users":
        data = cast(List[User], db.list_users())
        return {
            "data": [user.model_dump(exclude={"hashed_password"}) for user in data],
            "count": len(data),
        }
    else:  # table == "orders"
        data = cast(List[Order], db.list_orders())
        return {"data": [order.model_dump() for order in data], "count": len(data)}
