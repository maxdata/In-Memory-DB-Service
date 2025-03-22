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
    "password": "testpassword123"  # Password is added since it's required but not in sample data
}

test_order = sample_data["orders"][0]

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
    assert response.status_code == 201
    assert response.json()["email"] == test_user["email"]
    assert response.json()["full_name"] == test_user["full_name"]
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
    assert response.status_code == 201
    assert response.json()["amount"] == test_order["amount"]
    assert response.json()["description"] == test_order["description"]
    assert response.json()["status"] == test_order["status"]
    return response.json()["id"]

def test_create_user():
    """
    Test: User Creation
    """
    print("\nDebug: Starting user creation test")
    print(f"Debug: Using test data: {json.dumps(test_user, indent=2)}")
    
    response = client.post("/api/v1/users", json=test_user)
    print(f"Debug: Response status: {response.status_code}")
    print(f"Debug: Response body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    print("Debug: User creation test completed successfully")

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

@pytest.mark.parametrize("test_case", [
    {"name": "Basic update", "update": {"full_name": "John Updated"}},
    {"name": "Email update", "update": {"email": "updated@example.com"}},
    {"name": "Full update", "update": {
        "full_name": "John Complete Update",
        "email": "complete@example.com",
        "password": "newpass123"
    }}
])
def test_update_user_variations(user_id, test_case):
    """
    Test: User Update Variations
    Tests different combinations of field updates
    """
    print(f"\nDebug: Starting update test case: {test_case['name']}")
    print(f"Debug: Update data: {json.dumps(test_case['update'], indent=2)}")
    
    response = client.patch(f"/api/v1/users/{user_id}", json=test_case['update'])
    print(f"Debug: Response status: {response.status_code}")
    print(f"Debug: Response body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    for key, value in test_case['update'].items():
        if key != 'password':  # password is not returned in response
            assert data[key] == value
    print(f"Debug: Update test case '{test_case['name']}' completed successfully")

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
    """
    print("\nDebug: Starting user listing test")
    print(f"Debug: Creating {len(sample_user_data)} sample users")
    
    # Create additional sample users
    for i, user in enumerate(sample_user_data[1:], 1):
        print(f"Debug: Creating user {i}/{len(sample_user_data)-1}")
        user_data = {
            "email": user["email"],
            "full_name": user["full_name"],
            "password": "testpassword123"
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
        print(f"Debug: User {i} created successfully")
    
    print("Debug: Fetching user list")
    response = client.get("/api/v1/users")
    print(f"Debug: Response status: {response.status_code}")
    
    assert response.status_code == 200
    users_response = response.json()
    print(f"Debug: Found {users_response['count']} users")
    
    assert "data" in users_response
    assert "count" in users_response
    assert users_response["count"] >= len(sample_user_data)
    users = users_response["data"]
    assert len(users) >= len(sample_user_data)
    print("Debug: User listing test completed successfully")

def test_get_user_orders(user_id, order_id, sample_order_data):
    """
    Test: User-Orders Relationship
    
    Verifies that:
    1. Can retrieve all orders for a specific user
    2. Orders are correctly associated with the user
    3. Order details are complete and accurate
    4. Response includes all order fields
    """
    # Create an additional order for the user
    order_data = {
        "amount": 49.99,
        "description": "Second Test Product",
        "status": "pending",
        "user_id": user_id
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    
    # Get all orders for the user
    response = client.get(f"/api/v1/users/{user_id}/orders")
    assert response.status_code == 200
    orders_response = response.json()
    assert "data" in orders_response
    assert "count" in orders_response
    assert orders_response["count"] == 2
    orders = orders_response["data"]
    assert len(orders) == 2
    # Verify both orders are present
    assert any(order["amount"] == test_order["amount"] for order in orders)
    assert any(order["amount"] == order_data["amount"] for order in orders)

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
    assert "password" not in user  # Password should not be returned

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

def test_list_orders(user_id, order_id, sample_order_data):
    """
    Test: Order Listing
    
    Verifies that:
    1. Can list all orders
    2. Response includes count and data
    3. Order details are complete
    """
    print("\nDebug: Starting order listing test")
    
    # Create additional orders
    for order in sample_order_data[1:3]:  # Create 2 more orders
        order_data = {**order, "user_id": user_id}
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 201
        print(f"Debug: Created additional order with ID: {response.json()['id']}")
    
    # Get all orders
    response = client.get("/api/v1/orders")
    print(f"Debug: Response status: {response.status_code}")
    
    assert response.status_code == 200
    orders_response = response.json()
    print(f"Debug: Found {orders_response['count']} orders")
    
    assert "data" in orders_response
    assert "count" in orders_response
    assert orders_response["count"] >= 3  # At least 3 orders (1 from fixture + 2 new)
    orders = orders_response["data"]
    assert len(orders) >= 3
    print("Debug: Order listing test completed successfully")

@pytest.mark.parametrize("test_case", [
    {"name": "Update status", "update": {"status": "shipped"}},
    {"name": "Update amount", "update": {"amount": 150.99}},
    {"name": "Update description", "update": {"description": "Updated order description"}},
    {"name": "Full update", "update": {
        "status": "delivered",
        "amount": 199.99,
        "description": "Completely updated order"
    }}
])
def test_update_order_variations(order_id, test_case):
    """
    Test: Order Update Variations
    Tests different combinations of field updates
    """
    print(f"\nDebug: Starting update test case: {test_case['name']}")
    print(f"Debug: Update data: {json.dumps(test_case['update'], indent=2)}")
    
    response = client.patch(f"/api/v1/orders/{order_id}", json=test_case['update'])
    print(f"Debug: Response status: {response.status_code}")
    print(f"Debug: Response body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    for key, value in test_case['update'].items():
        assert data[key] == value
    print(f"Debug: Update test case '{test_case['name']}' completed successfully")

def test_delete_order(order_id):
    """
    Test: Order Deletion
    
    Verifies that:
    1. Can delete an existing order
    2. Response indicates successful deletion
    3. Returns boolean true on success
    """
    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify order is deleted
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 404

def test_health_check():
    """
    Test: Health Check Endpoint
    
    Verifies that:
    1. Health check endpoint is accessible
    2. Returns 200 OK status
    3. Returns expected health status
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_readiness_check():
    """
    Test: Readiness Check Endpoint
    
    Verifies that:
    1. Readiness check endpoint is accessible
    2. Returns 200 OK status
    3. Returns expected readiness status
    """
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ready" 