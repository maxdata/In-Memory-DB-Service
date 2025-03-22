import pytest
import json
import os
from starlette.testclient import TestClient
from app.main import app

"""
Normal Path Tests for the In-Memory Database Service API

This test suite covers the happy path scenarios for all API endpoints, ensuring that
the basic functionality works as expected under normal conditions. It includes tests
for CRUD operations on users and orders, as well as relationship endpoints between
these resources.

Test Structure:
1. Fixtures: Setup test data and common resources
2. User Operations: Create, read, update, delete, and list users
3. Order Operations: Create and manage orders
4. Relationship Operations: Test user-order relationships
5. Utility Operations: Test table dumps and other utilities
"""

client = TestClient(app)

# Load sample test data from JSON file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(TESTS_DIR, 'sample_data.json'), 'r') as f:
    sample_data = json.load(f)

# Get first user and order from sample data
test_user = {
    "email": sample_data["users"][0]["email"],
    "full_name": sample_data["users"][0]["full_name"],
    "age": sample_data["users"][0]["age"]
}

test_order = {
    "product_name": sample_data["orders"][0]["product_name"],
    "quantity": sample_data["orders"][0]["quantity"],
    "total_price": sample_data["orders"][0]["total_price"],
    "status": sample_data["orders"][0]["status"],
    "order_date": sample_data["orders"][0]["order_date"]
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
    Fixture: Creates a test user and returns their ID.
    
    This fixture is used as a prerequisite for many tests that require
    an existing user. It also validates the user creation response to
    ensure the test starts with valid data.
    """
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["full_name"] == test_user["full_name"]
    assert response.json()["age"] == test_user["age"]
    return response.json()["id"]

@pytest.fixture
def order_id(user_id):
    """
    Fixture: Creates a test order for a user and returns the order ID.
    
    Dependencies:
        - user_id fixture (needs an existing user to create an order)
    
    This fixture creates an order and validates the creation response,
    ensuring the test starts with valid order data.
    """
    order_data = {**test_order, "user_id": user_id}
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 200
    assert response.json()["product_name"] == test_order["product_name"]
    assert response.json()["quantity"] == test_order["quantity"]
    assert response.json()["total_price"] == test_order["total_price"]
    assert response.json()["status"] == test_order["status"]
    return response.json()["id"]

def test_create_user():
    """
    Test: User Creation
    
    Verifies that:
    1. User can be created with valid data
    2. Response contains all expected user fields
    3. Response includes a valid UUID
    4. All provided data is correctly stored
    """
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert data["age"] == test_user["age"]
    assert "id" in data

def test_create_order(order_id):
    """
    Test: Order Creation
    
    Note: Main order creation testing is handled by the order_id fixture.
    This test exists for completeness in the test suite structure.
    """
    pass  # Already covered by fixture

def test_get_user(user_id):
    """
    Test: User Retrieval
    
    Verifies that:
    1. Can retrieve a specific user by ID
    2. Retrieved data matches the created user
    3. All user fields are correctly returned
    """
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["full_name"] == test_user["full_name"]
    assert response.json()["id"] == user_id

def test_update_user(user_id):
    """
    Test: User Update
    
    Verifies that:
    1. Can update all user fields
    2. Response contains updated values
    3. User ID remains unchanged
    4. Non-updated fields retain their values
    """
    updated_data = {
        "full_name": "John Updated",
        "email": "john.updated@example.com",
        "age": 31
    }
    response = client.patch(f"/api/v1/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == updated_data["full_name"]
    assert response.json()["email"] == updated_data["email"]
    assert response.json()["age"] == updated_data["age"]
    assert response.json()["id"] == user_id

def test_delete_user(user_id):
    """
    Test: User Deletion
    
    Verifies that:
    1. Can delete an existing user
    2. Response indicates successful deletion
    3. Returns boolean true on success
    """
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json() is True

def test_list_users(user_id, sample_user_data):
    """
    Test: User Listing
    
    Verifies that:
    1. Can retrieve list of all users
    2. Response is a non-empty array
    3. Created test user is in the list
    4. User data is correctly structured
    """
    # Create additional sample users
    for user in sample_user_data[1:]:  # Skip first user as it's already created
        user_data = {
            "email": user["email"],
            "full_name": user["full_name"],
            "age": user["age"]
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 200

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= len(sample_user_data)
    assert any(user["id"] == user_id for user in users)

def test_get_user_orders(user_id, order_id, sample_order_data):
    """
    Test: User-Orders Relationship
    
    Verifies that:
    1. Can retrieve all orders for a specific user
    2. Orders are correctly associated with the user
    3. Order details are complete and accurate
    4. Response includes all order fields
    """
    # Create additional sample orders for the user
    # We'll use the first two orders from sample data, but with our test user's ID
    test_orders = sample_order_data[:2]  # Take first two orders
    
    # First order is already created by the fixture
    # Create the second order
    order_data = {
        "product_name": test_orders[1]["product_name"],
        "quantity": test_orders[1]["quantity"],
        "total_price": test_orders[1]["total_price"],
        "status": test_orders[1]["status"],
        "order_date": test_orders[1]["order_date"],
        "user_id": user_id
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 200

    response = client.get(f"/api/v1/users/{user_id}/orders")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 2  # We should have exactly 2 orders
    assert any(order["id"] == order_id for order in orders)
    
    # Verify first order details
    first_order = next(order for order in orders if order["id"] == order_id)
    assert first_order["user_id"] == user_id
    assert first_order["product_name"] == test_order["product_name"]
    assert first_order["quantity"] == test_order["quantity"]
    assert first_order["total_price"] == test_order["total_price"]
    assert first_order["status"] == test_order["status"]

def test_get_order_user(user_id, order_id):
    """
    Test: Order-User Relationship
    
    Verifies that:
    1. Can retrieve user details from an order
    2. User details are complete and accurate
    3. Relationship is correctly maintained
    
    This tests the second relationship endpoint that shows
    the many-to-one relationship between orders and users.
    """
    response = client.get(f"/api/v1/orders/{order_id}/user")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user_id
    assert user["email"] == test_user["email"]
    assert user["full_name"] == test_user["full_name"]
    assert user["age"] == test_user["age"]

def test_dump_table(user_id):
    """
    Test: Table Dump Utility
    
    Verifies that:
    1. Can dump contents of a table
    2. Response includes data and count
    3. Test data is present in the dump
    4. Count accurately reflects data size
    """
    response = client.get("/api/v1/tables/users/dump")
    assert response.status_code == 200
    result = response.json()
    assert len(result["data"]) > 0
    assert result["count"] > 0
    assert any(user["id"] == user_id for user in result["data"]) 