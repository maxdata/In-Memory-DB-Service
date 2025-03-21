"""
Utility functions for the in-memory database service.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID, uuid4

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO format with timezone."""
    return dt.isoformat() + "Z"

def parse_uuid(uuid_str: str) -> UUID:
    """Parse a UUID string into a UUID object."""
    try:
        return UUID(uuid_str)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {uuid_str}") from e

def generate_record_id() -> str:
    """Generate a unique record ID."""
    return str(uuid4())

def validate_table_name(table: str) -> str:
    """Validate and normalize table name."""
    if not table or not isinstance(table, str):
        raise ValueError("Table name must be a non-empty string")
    return table.lower()

def validate_record_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate record data."""
    if not isinstance(data, dict):
        raise ValueError("Record data must be a dictionary")
    if not data:
        raise ValueError("Record data cannot be empty")
    return data

def validate_join_key(table1: str, table2: str, key: str) -> None:
    """Validate join operation parameters."""
    # Validate table names
    validate_table_name(table1)
    validate_table_name(table2)
    
    # Validate tables are different
    if table1 == table2:
        raise ValueError("Cannot join a table with itself")
    
    # Validate join key exists
    if not key:
        raise ValueError("Join key cannot be empty")

def perform_join(table1_data: List[Dict[str, Any]], 
                table2_data: List[Dict[str, Any]], 
                key: str) -> List[Dict[str, Any]]:
    """
    Perform an inner join between two tables based on a key.
    
    Args:
        table1_data: List of records from first table
        table2_data: List of records from second table
        key: The key to join on
        
    Returns:
        List of joined records
    """
    result = []
    
    # Create lookup dictionary for second table
    table2_lookup = {str(record.get(key)): record for record in table2_data}
    
    # Perform join
    for record1 in table1_data:
        key_val = str(record1.get(key))
        if key_val in table2_lookup:
            joined_record = {**record1, **table2_lookup[key_val]}
            result.append(joined_record)
    
    return result

def format_error_response(error: Exception) -> Dict[str, Any]:
    """Format error response."""
    return {
        "error": type(error).__name__,
        "detail": str(error),
        "timestamp": format_datetime(datetime.utcnow())
    }

def format_success_response(data: Any) -> Dict[str, Any]:
    """Format success response."""
    return {
        "data": data,
        "timestamp": format_datetime(datetime.utcnow())
    }

def validate_record_id(record_id: str) -> str:
    """Validate record ID format."""
    try:
        UUID(record_id)
        return record_id
    except ValueError as e:
        raise ValueError(f"Invalid record ID format: {record_id}") from e
