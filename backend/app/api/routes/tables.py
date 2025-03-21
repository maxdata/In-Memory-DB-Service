from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import User, Order, UserOrder, Message
from app.api.deps import MemoryDBDep

router = APIRouter(prefix="/api/v1", tags=["tables"])

# Map table names to their corresponding models
TABLE_MODELS = {
    "users": User,
    "orders": Order
}

class GenericCreate(BaseModel):
    data: Dict[str, Any]

@router.post("/data/{table}", response_model=Dict[str, Any])
def add_record(*, db: MemoryDBDep, table: str, record: GenericCreate) -> Any:
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
        elif table == "orders":
            order = Order(**record.data)
            result = db.add_order(order)
            return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/data/{table}/{record_id}", response_model=Dict[str, Any])
def update_record(*, db: MemoryDBDep, table: str, record_id: UUID, record: GenericCreate) -> Any:
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
        elif table == "orders":
            result = db.update_order(record_id, record.data)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/data/{table}/{record_id}", response_model=Message)
def delete_record(*, db: MemoryDBDep, table: str, record_id: UUID) -> Any:
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

@router.get("/join/{table1}/{table2}/{key}", response_model=Dict[str, Any])
def join_tables(*, db: MemoryDBDep, table1: str, table2: str, key: str) -> Any:
    """
    Join two tables based on a common key.
    Currently supports joining users and orders tables.
    """
    if table1 not in TABLE_MODELS or table2 not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail="One or both tables not found")
    
    # Currently only supports users-orders join
    if {table1, table2} == {"users", "orders"}:
        joined_data = db.join_user_orders()
        return {
            "data": [item.model_dump() for item in joined_data],
            "count": len(joined_data)
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Currently only supports joining users and orders tables"
        )

@router.get("/dump/{table}", response_model=Dict[str, Any])
def dump_table(*, db: MemoryDBDep, table: str) -> Any:
    """
    Dump all contents of the specified table.
    """
    if table not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")
    
    if table == "users":
        data = db.list_users()
        return {
            "data": [user.model_dump(exclude={"hashed_password"}) for user in data],
            "count": len(data)
        }
    elif table == "orders":
        data = db.list_orders()
        return {
            "data": [order.model_dump() for order in data],
            "count": len(data)
        } 