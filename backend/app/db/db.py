from datetime import datetime
from typing import Any, cast
from uuid import UUID, uuid4

from app.db.initial_data import get_sample_data
from app.models.user import User, UserOrder
from app.models.order import Order

#


class MemoryDB:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}
        self.orders: dict[UUID, Order] = {}

    def init_db(self) -> None:
        """Initialize the database with sample data."""
        sample_data = get_sample_data()

        # Add users
        for user_data in sample_data["users"]:
            user_dict = cast(dict[str, Any], user_data)
            user = User(
                id=UUID(user_dict["id"]),
                email=user_dict["email"],
                full_name=user_dict["full_name"],
                password=user_dict["hashed_password"],
                created_at=datetime.fromisoformat(user_dict["created_at"]),
            )
            self.users[user.id] = user

        # Add orders
        for order_data in sample_data["orders"]:
            order_dict = cast(dict[str, Any], order_data)
            order = Order(
                id=UUID(order_dict["id"]),
                user_id=UUID(order_dict["user_id"]),
                product_name=order_dict["product_name"],
                quantity=order_dict["quantity"],
                total_price=order_dict["total_price"],
                created_at=datetime.fromisoformat(order_dict["created_at"]),
            )
            self.orders[order.id] = order

    def add_user(self, user: User) -> User:
        """Add a new user to the database."""
        if not user.id:
            user.id = uuid4()
        if not user.created_at:
            user.created_at = datetime.now()
        self.users[user.id] = user
        return user

    def add_order(self, order: Order) -> Order:
        """Add a new order to the database."""
        if not order.id:
            order.id = uuid4()
        if not order.created_at:
            order.created_at = datetime.now()
        self.orders[order.id] = order
        return order

    def get_user(self, user_id: UUID) -> User | None:
        """Get a user by ID."""
        return self.users.get(user_id)

    def get_order(self, order_id: UUID) -> Order | None:
        """Get an order by ID."""
        return self.orders.get(order_id)

    def list_users(self) -> list[User]:
        """List all users."""
        return list(self.users.values())

    def list_orders(self) -> list[Order]:
        """List all orders."""
        return list(self.orders.values())

    def update_user(self, user_id: UUID, data: dict[str, Any]) -> User | None:
        """Update a user's data."""
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user

    def update_order(self, order_id: UUID, data: dict[str, Any]) -> Order | None:
        """Update an order's data."""
        if order_id not in self.orders:
            return None
        order = self.orders[order_id]
        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)
        return order

    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user and their associated orders."""
        # Only delete user if they have no orders
        if user_id in self.users:
            # TODO: change to first get all the orders and then delete them
            # TODO: first delete the orders and then the user

            del self.users[user_id]
            self.orders = {k: v for k, v in self.orders.items() if v.user_id != user_id}
            return True
        return False

    def delete_order(self, order_id: UUID) -> bool:
        """Delete an order by ID."""
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False