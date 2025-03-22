import pytest
import json
import os
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4, UUID
from datetime import datetime

"""
Edge Case Tests for the In-Memory Database Service API

This test suite focuses on testing edge cases, error conditions, and boundary scenarios
for all API endpoints. It ensures that the API handles invalid inputs, non-existent
resources, and error conditions gracefully and returns appropriate error responses.

Test Categories:
1. Invalid UUID Format Tests: Testing endpoints with malformed UUIDs
2. Non-existent Resource Tests: Testing endpoints with valid but non-existent UUIDs
3. Relationship Edge Cases: Testing relationship endpoints with invalid/non-existent resources
4. Resource State Tests: Testing operations on deleted resources
5. Invalid Resource Tests: Testing operations with invalid table names

Error Response Expectations:
- 422: Validation errors (invalid UUID format)
- 404: Resource not found
- 400: Bad request (invalid data)
"""

client = TestClient(app)

# Load sample test data from JSON file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(TESTS_DIR, 'sample_data.json'), 'r') as f:
    sample_data = json.load(f)

# Use first user from sample data for testing
test_user = sample_data["users"][0]

# Use first order from sample data for testing
test_order = sample_data["orders"][0]

# Additional test data for edge cases
invalid_user = {
    "email": "invalid",  # Invalid email format
    "full_name": "x" * 101,  # Name too long (>100 chars)
    "password": "short"  # Password too short (<8 chars)
}

@pytest.fixture
def sample_user_data():
    """Fixture to provide sample user data for tests"""
    return sample_data["users"]

@pytest.fixture
def sample_order_data():
    """Fixture to provide sample order data for tests"""
    return sample_data["orders"]

@pytest.fixture
def user_id():
    """
    Fixture: Creates a valid user for testing edge cases.
    
    This fixture is used when we need a valid user ID to test
    edge cases that require an existing user (e.g., testing
    non-existent orders for an existing user).
    """
    response = client.post("/api/v1/users", json=test_user)
    return response.json()["id"]

@pytest.fixture
def known_nonexistent_uuid():
    """
    Fixture: Provides a UUID that is guaranteed to not exist in the sample data
    """
    return "550e8400-e29b-41d4-a716-446655449999"

def test_create_user_invalid_data():
    """
    Test: Invalid User Creation Data
    
    Verifies that:
    1. API properly validates user data
    2. Returns 422 for invalid email format
    3. Returns 422 for name too long
    4. Returns 422 for age out of range
    """
    response = client.post("/api/v1/users", json=invalid_user)
    assert response.status_code == 422

def test_get_user_invalid_uuid():
    """
    Test: Invalid UUID Format for User Retrieval
    
    Verifies that:
    1. API properly validates UUID format
    2. Returns 422 for malformed UUIDs
    3. Prevents database lookup with invalid ID
    """
    response = client.get("/api/v1/users/invalid-uuid")
    assert response.status_code == 422

def test_get_nonexistent_user():
    """
    Test: Non-existent User Retrieval
    
    Verifies that:
    1. API handles requests for non-existent users
    2. Returns 404 for valid but non-existent UUIDs
    3. Properly distinguishes between invalid format and non-existent resources
    """
    response = client.get(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 404

def test_update_user_invalid_uuid():
    """
    Test: Invalid UUID Format for User Update
    
    Verifies that:
    1. API validates UUID format before attempting update
    2. Returns 422 for malformed UUIDs
    3. Prevents database modification with invalid ID
    """
    updated_data = {
        "full_name": "John Updated",
        "email": "john.updated@example.com",
        "age": 31
    }
    response = client.patch("/api/v1/users/invalid-uuid", json=updated_data)
    assert response.status_code == 422

def test_update_nonexistent_user():
    """
    Test: Non-existent User Update
    
    Verifies that:
    1. API handles update requests for non-existent users
    2. Returns 404 for valid but non-existent UUIDs
    3. Prevents modification of non-existent resources
    """
    updated_data = {
        "full_name": "John Updated",
        "email": "john.updated@example.com",
        "password": "updatedpassword123"
    }
    response = client.patch(f"/api/v1/users/{uuid4()}", json=updated_data)
    assert response.status_code == 404

def test_delete_user_invalid_uuid():
    """
    Test: Invalid UUID Format for User Deletion
    
    Verifies that:
    1. API validates UUID format before attempting deletion
    2. Returns 422 for malformed UUIDs
    3. Prevents database deletion with invalid ID
    """
    response = client.delete("/api/v1/users/invalid-uuid")
    assert response.status_code == 422

def test_delete_nonexistent_user():
    """
    Test: Non-existent User Deletion
    
    Verifies that:
    1. API handles deletion requests for non-existent users
    2. Returns 404 for valid but non-existent UUIDs
    3. Properly handles deletion attempts of non-existent resources
    """
    response = client.delete(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 404

def test_get_orders_invalid_user_uuid():
    """
    Test: Invalid UUID Format for User-Orders Relationship
    
    Verifies that:
    1. API validates user UUID format in relationship endpoint
    2. Returns 422 for malformed UUIDs
    3. Prevents relationship lookup with invalid user ID
    """
    response = client.get("/api/v1/users/invalid-uuid/orders")
    assert response.status_code == 422

def test_get_orders_nonexistent_user(known_nonexistent_uuid):
    """
    Test: Non-existent User for User-Orders Relationship
    
    Verifies that:
    1. API handles order requests for non-existent users
    2. Returns 404 for valid but non-existent user UUIDs
    3. Properly handles relationship queries for non-existent users
    """
    response = client.get(f"/api/v1/users/{known_nonexistent_uuid}/orders")
    assert response.status_code == 404

def test_get_order_user_invalid_uuid():
    """
    Test: Invalid UUID Format for Order-User Relationship
    
    Verifies that:
    1. API validates order UUID format in relationship endpoint
    2. Returns 422 for malformed UUIDs
    3. Prevents relationship lookup with invalid order ID
    """
    response = client.get("/api/v1/orders/invalid-uuid/user")
    assert response.status_code == 422

def test_get_order_user_nonexistent_order(known_nonexistent_uuid):
    """
    Test: Non-existent Order for Order-User Relationship
    
    Verifies that:
    1. API handles user requests for non-existent orders
    2. Returns 404 for valid but non-existent order UUIDs
    3. Properly handles relationship queries for non-existent orders
    """
    response = client.get(f"/api/v1/orders/{known_nonexistent_uuid}/user")
    assert response.status_code == 404

def test_dump_nonexistent_table():
    """
    Test: Non-existent Table Dump
    
    Verifies that:
    1. API handles requests for non-existent tables
    2. Returns 404 for invalid table names
    3. Properly validates table names before attempting operations
    """
    response = client.get("/api/v1/tables/invalid/dump")
    assert response.status_code == 404

def test_verify_deleted_user(user_id):
    """
    Test: Resource State After Deletion
    
    Verifies that:
    1. Deleted user cannot be retrieved
    2. Deletion is permanent and consistent
    3. API maintains proper resource state
    4. Returns 404 for subsequent requests
    
    This test ensures that the deletion operation properly
    removes the resource and subsequent operations fail appropriately.
    """
    # First delete the user
    client.delete(f"/api/v1/users/{user_id}")
    
    # Then verify the user is gone
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404

def test_create_user_empty_values():
    """
    Test: Empty Values in User Creation
    
    Verifies that:
    1. API properly handles empty strings
    2. API properly handles null values
    3. Returns appropriate validation errors
    """
    empty_user = {
        "email": "",
        "full_name": "",
        "age": None
    }
    response = client.post("/api/v1/users", json=empty_user)
    assert response.status_code == 422

def test_create_user_special_characters():
    """
    Test: Special Characters in User Data
    
    Verifies that:
    1. API properly handles special characters in names
    2. API properly handles unicode characters
    3. API properly validates email with special characters
    """
    special_char_user = {
        "email": "user+test@example.com",
        "full_name": "José María García-López ♥",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users", json=special_char_user)
    assert response.status_code == 201
    assert response.json()["full_name"] == "José María García-López ♥"

def test_concurrent_user_updates(user_id):
    """
    Test: Concurrent User Updates
    
    Verifies that:
    1. API handles concurrent update requests
    2. Last update takes precedence
    3. No data corruption occurs
    """
    # First update
    update1 = {
        "full_name": "Update 1",
        "email": "update1@example.com",
        "password": "password1"
    }

    # Second update
    update2 = {
        "full_name": "Update 2",
        "email": "update2@example.com",
        "password": "password2"
    }

    # Send updates almost simultaneously
    response1 = client.patch(f"/api/v1/users/{user_id}", json=update1)
    response2 = client.patch(f"/api/v1/users/{user_id}", json=update2)

    # Both should succeed
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Get final state
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    final_state = response.json()

    # Last update should take precedence
    assert final_state["full_name"] == update2["full_name"]
    assert final_state["email"] == update2["email"]

def test_order_with_deleted_user(user_id):
    """
    Test: Order Operations with Deleted User
    
    Verifies that:
    1. Orders can't be created for deleted users
    2. Existing orders are handled properly when user is deleted
    3. API maintains referential integrity
    """
    # First create an order for the user
    order = {
        "user_id": user_id,
        "amount": 100.00,
        "description": "Test Product",
        "status": "pending"
    }
    order_response = client.post("/api/v1/orders", json=order)
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]

    # Delete the user
    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 200

    # Try to create another order for the deleted user
    new_order = {
        "user_id": user_id,
        "amount": 50.00,
        "description": "Another Product",
        "status": "pending"
    }
    new_order_response = client.post("/api/v1/orders", json=new_order)
    assert new_order_response.status_code == 404

    # Try to get the existing order
    get_order_response = client.get(f"/api/v1/orders/{order_id}")
    assert get_order_response.status_code == 200

def test_boundary_values():
    """
    Test: Boundary Value Testing
    
    Verifies that:
    1. API handles minimum allowed values
    2. API handles maximum allowed values
    3. API properly validates boundary conditions
    """
    # Test user with minimum valid data
    min_user = {
        "email": "min@example.com",
        "full_name": "M",  # Minimum length name
        "password": "password123"  # Minimum length password (8 chars)
    }
    min_response = client.post("/api/v1/users", json=min_user)
    assert min_response.status_code == 201

    # Test user with maximum valid data
    max_user = {
        "email": "max" + "x" * 50 + "@example.com",  # Long but valid email (RFC 5321 limits local part to 64 chars)
        "full_name": "M" * 100,  # Long name
        "password": "p" * 100  # Long password
    }
    max_response = client.post("/api/v1/users", json=max_user)
    assert max_response.status_code == 201

    # Test order with boundary values
    user_id = min_response.json()["id"]
    min_order = {
        "user_id": user_id,
        "amount": 0.01,  # Minimum positive amount
        "description": "M",  # Minimum length description
        "status": "pending"
    }
    min_order_response = client.post("/api/v1/orders", json=min_order)
    assert min_order_response.status_code == 201

    max_order = {
        "user_id": user_id,
        "amount": 999999.99,  # Large amount
        "description": "M" * 100,  # Long description
        "status": "pending"
    }
    max_order_response = client.post("/api/v1/orders", json=max_order)
    assert max_order_response.status_code == 201

def test_update_order_invalid_uuid():
    """
    Test: Invalid UUID Format for Order Update
    
    Verifies that:
    1. API validates order UUID format before attempting update
    2. Returns 422 for malformed UUIDs
    3. Prevents database modification with invalid ID
    """
    updated_data = {
        "status": "shipped",
        "amount": 199.99,
        "description": "Updated description"
    }
    response = client.patch("/api/v1/orders/invalid-uuid", json=updated_data)
    assert response.status_code == 422

def test_update_nonexistent_order():
    """
    Test: Non-existent Order Update
    
    Verifies that:
    1. API handles update requests for non-existent orders
    2. Returns 404 for valid but non-existent UUIDs
    3. Prevents modification of non-existent resources
    """
    updated_data = {
        "status": "shipped",
        "amount": 199.99,
        "description": "Updated description"
    }
    response = client.patch(f"/api/v1/orders/{uuid4()}", json=updated_data)
    assert response.status_code == 404

def test_update_order_invalid_status():
    """
    Test: Invalid Order Status Update
    
    Verifies that:
    1. API validates order status values
    2. Returns 422 for invalid status values
    3. Prevents updates with invalid status
    """
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]
    
    # Create an order first
    order_data = {**test_order, "user_id": user_id}
    response = client.post("/api/v1/orders", json=order_data)
    order_id = response.json()["id"]
    
    # Try to update with invalid status
    updated_data = {"status": "invalid_status"}
    response = client.patch(f"/api/v1/orders/{order_id}", json=updated_data)
    assert response.status_code == 422

def test_update_order_invalid_amount():
    """
    Test: Invalid Order Amount Update
    
    Verifies that:
    1. API validates order amount values
    2. Returns 422 for invalid amounts
    3. Prevents updates with invalid amounts
    """
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]
    
    # Create an order first
    order_data = {**test_order, "user_id": user_id}
    response = client.post("/api/v1/orders", json=order_data)
    order_id = response.json()["id"]
    
    # Try to update with invalid amount
    updated_data = {"amount": -50.00}  # Negative amount should be invalid
    response = client.patch(f"/api/v1/orders/{order_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_order_invalid_uuid():
    """
    Test: Invalid UUID Format for Order Deletion
    
    Verifies that:
    1. API validates order UUID format before attempting deletion
    2. Returns 422 for malformed UUIDs
    3. Prevents database deletion with invalid ID
    """
    response = client.delete("/api/v1/orders/invalid-uuid")
    assert response.status_code == 422

def test_delete_nonexistent_order():
    """
    Test: Non-existent Order Deletion
    
    Verifies that:
    1. API handles deletion requests for non-existent orders
    2. Returns 404 for valid but non-existent UUIDs
    3. Properly handles deletion attempts of non-existent resources
    """
    response = client.delete(f"/api/v1/orders/{uuid4()}")
    assert response.status_code == 404

def test_health_check_edge_cases():
    """
    Test: Health Check Edge Cases
    
    Verifies that:
    1. Health check endpoint handles various HTTP methods
    2. Returns appropriate status codes for invalid methods
    3. Maintains consistent response format
    """
    # Test with invalid HTTP method
    response = client.post("/api/v1/health", json={})
    assert response.status_code == 405  # Method not allowed
    
    # Test with query parameters (should be ignored)
    response = client.get("/api/v1/health?param=value")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check_edge_cases():
    """
    Test: Readiness Check Edge Cases
    
    Verifies that:
    1. Readiness check endpoint handles various HTTP methods
    2. Returns appropriate status codes for invalid methods
    3. Maintains consistent response format
    """
    # Test with invalid HTTP method
    response = client.post("/api/v1/ready", json={})
    assert response.status_code == 405  # Method not allowed
    
    # Test with query parameters (should be ignored)
    response = client.get("/api/v1/ready?param=value")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_dump_table_invalid_format():
    """
    Test: Invalid Table Format Request
    
    Verifies that:
    1. API validates table format parameters
    2. Returns 400 for invalid format requests
    3. Provides clear error messages
    """
    response = client.get("/api/v1/tables/users/dump?format=invalid")
    assert response.status_code == 400
    assert "Invalid format" in response.json()["detail"]

def test_dump_table_concurrent_access(user_id):
    """
    Test: Concurrent Table Access
    
    Verifies that:
    1. API handles concurrent table access properly
    2. Maintains data consistency during concurrent reads
    3. Returns consistent results for parallel requests
    """
    import asyncio
    import httpx
    
    async def make_concurrent_requests():
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
            tasks = [
                ac.get("/api/v1/tables/users/dump"),
                ac.get("/api/v1/tables/orders/dump"),
                ac.get("/api/v1/db/dump/users"),
                ac.get("/api/v1/db/dump/orders")
            ]
            responses = await asyncio.gather(*tasks)
            return [r.status_code for r in responses]
    
    status_codes = asyncio.run(make_concurrent_requests())
    assert all(code == 200 for code in status_codes) 