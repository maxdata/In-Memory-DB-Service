"""Tests for table operations and error cases in the in-memory database service."""

from fastapi.testclient import TestClient

from app.core.config import settings


def test_nonexistent_table(client: TestClient, setup_test_db):
    """Test operations on a non-existent table."""
    fake_table = "nonexistent_table"
    
    # Test get record
    response = client.get(
        f"{settings.API_V1_STR}/tables/{fake_table}/records/123"
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]
    
    # Test create record
    response = client.post(
        f"{settings.API_V1_STR}/tables/{fake_table}/records",
        json={"field": "value"}
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]
    
    # Test update record
    response = client.put(
        f"{settings.API_V1_STR}/tables/{fake_table}/records/123",
        json={"field": "value"}
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]
    
    # Test delete record
    response = client.delete(
        f"{settings.API_V1_STR}/tables/{fake_table}/records/123"
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]
    
    # Test dump table
    response = client.get(
        f"{settings.API_V1_STR}/tables/{fake_table}/dump"
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]


def test_invalid_join_parameters(client: TestClient, setup_test_db):
    """Test join operations with invalid parameters."""
    # Test join with non-existent table
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "nonexistent",
            "table2": "orders",
            "key": "user_id"
        }
    )
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]
    
    # Test join with invalid key
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "invalid_key"
        }
    )
    assert response.status_code == 400
    assert "Invalid join key" in response.json()["detail"]
    
    # Test join with same table
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "users",
            "key": "id"
        }
    )
    assert response.status_code == 400
    assert "Cannot join table with itself" in response.json()["detail"]


def test_invalid_record_data(client: TestClient, setup_test_db):
    """Test operations with invalid record data."""
    # Test create user with missing required field
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json={"password": "test123"}  # Missing email
    )
    assert response.status_code == 422  # Validation error
    
    # Test create order with invalid data types
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json={
            "product": 123,  # Should be string
            "quantity": "invalid",  # Should be integer
            "user_id": "test_id"
        }
    )
    assert response.status_code == 422  # Validation error
    
    # Test update with invalid data types
    response = client.put(
        f"{settings.API_V1_STR}/tables/orders/records/123",
        json={
            "quantity": "invalid"  # Should be integer
        }
    )
    assert response.status_code == 422  # Validation error


def test_empty_database_operations(client: TestClient):
    """Test operations on an empty database before initialization."""
    # Test dump users table
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    assert response.status_code == 200
    assert response.json() == []
    
    # Test dump orders table
    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    assert response.status_code == 200
    assert response.json() == []
    
    # Test join on empty tables
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "user_id"
        }
    )
    assert response.status_code == 200
    assert response.json() == []


def test_table_creation(client: TestClient, setup_test_db):
    """Test table creation and basic operations."""
    # Test creating a user record
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123"
    }
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json=user_data
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Test creating an order record
    order_data = {
        "user_id": user_id,
        "product_name": "Test Product",
        "quantity": 1,
        "total_price": 99.99,
        "status": "pending"
    }
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json=order_data
    )
    assert response.status_code == 201
    
    # Test retrieving the created records
    response = client.get(f"{settings.API_V1_STR}/tables/users/records/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    
    # Test dumping the tables
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_dump_users_table(client, sample_user):
    """Test dumping the users table."""
    response = client.get("/api/v1/dump/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] > 0
    assert len(data["data"]) == data["count"]
    
    # Verify user data is present
    user_found = False
    for user in data["data"]:
        if user["email"] == sample_user["email"]:
            user_found = True
            assert user["full_name"] == sample_user["full_name"]
            break
    assert user_found


def test_dump_orders_table(client, sample_order):
    """Test dumping the orders table."""
    response = client.get("/api/v1/dump/orders")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] > 0
    assert len(data["data"]) == data["count"]
    
    # Verify order data is present
    order_found = False
    for order in data["data"]:
        if order["id"] == str(sample_order["id"]):
            order_found = True
            assert order["product_name"] == sample_order["product_name"]
            assert order["quantity"] == sample_order["quantity"]
            break
    assert order_found


def test_dump_invalid_table(client):
    """Test dumping an invalid table."""
    response = client.get("/api/v1/dump/invalid_table")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower() 