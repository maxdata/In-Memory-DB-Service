"""Tests for input validation and error handling in the in-memory database service."""

from fastapi.testclient import TestClient

from app.core.config import settings

def test_invalid_user_payload(client: TestClient, setup_test_db):
    """Test validation of user creation payload."""
    # Test empty payload
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json={}
    )
    assert response.status_code == 422
    
    # Test missing required fields
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json={"password": "test123"}  # Missing email
    )
    assert response.status_code == 422
    
    # Test invalid email format
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json={
            "email": "not_an_email",
            "password": "test123"
        }
    )
    assert response.status_code == 422


def test_invalid_order_payload(client: TestClient, setup_test_db, user_id):
    """Test validation of order creation payload."""
    # Test empty payload
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json={}
    )
    assert response.status_code == 422
    
    # Test missing required fields
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json={"product": "Test Product"}  # Missing quantity and user_id
    )
    assert response.status_code == 422
    
    # Test invalid data types
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json={
            "product": 123,  # Should be string
            "quantity": "invalid",  # Should be integer
            "user_id": user_id
        }
    )
    assert response.status_code == 422
    
    # Test invalid quantity value
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json={
            "product": "Test Product",
            "quantity": -1,  # Should be positive
            "user_id": user_id
        }
    )
    assert response.status_code == 422


def test_invalid_update_payload(client: TestClient, setup_test_db, test_user):
    """Test validation of update operations."""
    # Test empty update payload
    response = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}",
        json={}
    )
    assert response.status_code == 422
    
    # Test invalid email format in update
    response = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}",
        json={"email": "not_an_email"}
    )
    assert response.status_code == 422


def test_invalid_id_format(client: TestClient, setup_test_db):
    """Test validation of ID parameters."""
    invalid_id = "not-a-valid-id"
    
    # Test invalid user ID
    response = client.get(
        f"{settings.API_V1_STR}/tables/users/records/{invalid_id}"
    )
    assert response.status_code == 422
    
    # Test invalid order ID
    response = client.get(
        f"{settings.API_V1_STR}/tables/orders/records/{invalid_id}"
    )
    assert response.status_code == 422


def test_invalid_join_parameters(client: TestClient, setup_test_db):
    """Test validation of join operation parameters."""
    # Test missing parameters
    response = client.get(f"{settings.API_V1_STR}/tables/join")
    assert response.status_code == 422
    
    # Test invalid table names
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "invalid_table",
            "table2": "orders",
            "key": "user_id"
        }
    )
    assert response.status_code == 404
    
    # Test invalid join key
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "invalid_key"
        }
    )
    assert response.status_code == 400


def test_concurrent_modifications(client: TestClient, setup_test_db, test_user):
    """Test handling of concurrent modifications."""
    # Try to update the same record twice in quick succession
    update_data = {"email": "new@example.com"}
    
    response1 = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}",
        json=update_data
    )
    assert response1.status_code == 200
    
    # Second update should still work (no versioning conflicts in in-memory db)
    update_data["email"] = "newer@example.com"
    response2 = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}",
        json=update_data
    )
    assert response2.status_code == 200
    assert response2.json()["email"] == "newer@example.com" 