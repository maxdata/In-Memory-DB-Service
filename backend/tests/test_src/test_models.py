import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import EmailStr, ValidationError

from app.models.user import User
from app.models.order import Order, UserOrder

def test_user_model_creation():
    """Test creating a User model with valid data"""
    user_id = str(uuid4())
    user_data = {
        "id": user_id,
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    user = User(**user_data)
    assert user.id == user_data["id"]
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.password == user_data["password"]
    assert user.is_active == user_data["is_active"]

def test_user_model_validation():
    """Test User model validation"""
    with pytest.raises(ValidationError):
        User(
            id=str(uuid4()),
            email="invalid-email",  # Invalid email format
            full_name="Test User",
            password="testpass123",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

def test_user_model_required_fields():
    """Test User model required fields"""
    with pytest.raises(ValidationError):
        User()  # Missing required fields

def test_order_model_creation():
    """Test creating an Order model with valid data"""
    order_data = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "description": "Test Product",
        "amount": 99.99,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    order = Order(**order_data)
    assert order.id == order_data["id"]
    assert order.user_id == order_data["user_id"]
    assert order.description == order_data["description"]
    assert order.amount == order_data["amount"]
    assert order.status == order_data["status"]

def test_order_model_validation():
    """Test Order model validation"""
    # Test invalid amount
    with pytest.raises(ValidationError):
        Order(
            id=str(uuid4()),
            user_id=str(uuid4()),
            description="Test Product",
            amount=-1.0,  # Invalid amount
            status="pending"
        )

def test_order_model_required_fields():
    """Test Order model required fields"""
    with pytest.raises(ValidationError):
        Order()  # Missing required fields

def test_order_status_transitions():
    """Test Order status transitions"""
    order = Order(
        id=str(uuid4()),
        user_id=str(uuid4()),
        description="Test Product",
        amount=99.99,
        status="pending"
    )
    
    # Test valid status transitions
    valid_statuses = ["processing", "shipped", "delivered", "cancelled"]
    for status in valid_statuses:
        order.status = status
        assert order.status == status

def test_user_order_model():
    """Test UserOrder model creation and validation"""
    user_order_data = {
        "user_id": str(uuid4()),
        "user_email": "test@example.com",
        "user_full_name": "Test User",
        "order_id": str(uuid4()),
        "description": "Test Product",
        "amount": 99.99,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    user_order = UserOrder(**user_order_data)
    assert user_order.user_id == user_order_data["user_id"]
    assert user_order.user_email == user_order_data["user_email"]
    assert user_order.user_full_name == user_order_data["user_full_name"]
    assert user_order.order_id == user_order_data["order_id"]
    assert user_order.description == user_order_data["description"]
    assert user_order.amount == user_order_data["amount"]
    assert user_order.status == user_order_data["status"]
    assert user_order.created_at == user_order_data["created_at"]

    # Test invalid email
    with pytest.raises(ValidationError):
        UserOrder(
            **{**user_order_data, "user_email": "invalid-email"}
        ) 