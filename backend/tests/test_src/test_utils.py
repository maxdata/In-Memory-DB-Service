import pytest
from datetime import datetime
from uuid import UUID

from app.utils import (
    format_datetime,
    parse_uuid,
    validate_table_name,
    validate_record_data,
    format_error_response,
    format_success_response,
    validate_record_id,
    perform_join,
    generate_record_id,
    validate_join_key
)

def test_datetime_formatting():
    """Test datetime formatting"""
    dt = datetime(2024, 3, 21, 12, 0, 0)
    formatted = format_datetime(dt)
    assert formatted == "2024-03-21T12:00:00Z"

def test_uuid_parsing():
    """Test UUID parsing"""
    # Test valid UUID
    uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    uuid = parse_uuid(uuid_str)
    assert isinstance(uuid, UUID)
    assert str(uuid) == uuid_str
    
    # Test invalid UUID
    with pytest.raises(ValueError, match="Invalid UUID format"):
        parse_uuid("invalid-uuid")

def test_generate_record_id():
    """Test record ID generation."""
    # Test that generated IDs are valid UUIDs
    record_id = generate_record_id()
    assert isinstance(UUID(record_id), UUID)
    
    # Test that generated IDs are unique
    record_id2 = generate_record_id()
    assert record_id != record_id2

def test_table_name_validation():
    """Test table name validation"""
    # Test valid table names
    assert validate_table_name("users") == "users"
    assert validate_table_name("ORDERS") == "orders"
    
    # Test invalid table names
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        validate_table_name("")
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        validate_table_name(None)

def test_record_data_validation():
    """Test record data validation"""
    # Test valid record data
    valid_data = {"id": "123", "name": "test"}
    assert validate_record_data(valid_data) == valid_data
    
    # Test invalid record data
    with pytest.raises(ValueError, match="Record data must be a dictionary"):
        validate_record_data("not a dict")
    with pytest.raises(ValueError, match="Record data cannot be empty"):
        validate_record_data({})

def test_validate_join_key():
    """Test join key validation."""
    # Test valid join operation
    validate_join_key("users", "orders", "user_id")
    
    # Test invalid table names
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        validate_join_key("", "orders", "user_id")
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        validate_join_key("users", "", "user_id")
    
    # Test same table join
    with pytest.raises(ValueError, match="Cannot join a table with itself"):
        validate_join_key("users", "users", "user_id")
    
    # Test empty join key
    with pytest.raises(ValueError, match="Join key cannot be empty"):
        validate_join_key("users", "orders", "")

def test_error_response_formatting():
    """Test error response formatting"""
    test_error = ValueError("Test error message")
    response = format_error_response(test_error)
    
    assert "error" in response
    assert response["error"] == "ValueError"
    assert response["detail"] == "Test error message"
    assert "timestamp" in response

def test_success_response_formatting():
    """Test success response formatting"""
    test_data = {"id": "123", "name": "test"}
    response = format_success_response(test_data)
    
    assert "data" in response
    assert response["data"] == test_data
    assert "timestamp" in response

def test_record_id_validation():
    """Test record ID validation"""
    # Test valid record ID
    valid_id = "123e4567-e89b-12d3-a456-426614174000"
    assert validate_record_id(valid_id) == valid_id
    
    # Test invalid record ID
    with pytest.raises(ValueError, match="Invalid record ID format"):
        validate_record_id("invalid-id")

def test_join_operations():
    """Test join operations"""
    table1_data = [
        {"id": "1", "name": "John", "dept_id": "D1"},
        {"id": "2", "name": "Jane", "dept_id": "D2"},
        {"id": "3", "name": "Bob", "dept_id": "D3"}
    ]

    table2_data = [
        {"dept_id": "D1", "department": "HR"},
        {"dept_id": "D2", "department": "IT"}
    ]

    joined_data = perform_join(table1_data, table2_data, "dept_id")
    
    # Verify join results
    assert len(joined_data) == 2  # Only records with matching dept_id
    assert joined_data[0]["name"] == "John"
    assert joined_data[0]["department"] == "HR"
    assert joined_data[1]["name"] == "Jane"
    assert joined_data[1]["department"] == "IT" 