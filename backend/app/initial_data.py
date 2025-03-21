"""Sample data for testing the in-memory database service."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, TypedDict, Union


class UserData(TypedDict):
    id: str
    email: str
    full_name: str
    age: int
    is_active: bool
    created_at: str
    updated_at: str


class OrderData(TypedDict):
    id: str
    user_id: str
    product_name: str
    quantity: int
    total_price: float
    status: str
    created_at: str
    updated_at: str


def load_sample_data() -> Dict[str, Union[List[UserData], List[OrderData]]]:
    """Load sample data from JSON file."""
    json_path = Path(__file__).parent / "sample_data.json"
    with open(json_path, "r") as f:
        return json.load(f)


def get_sample_data() -> Dict[str, Union[List[UserData], List[OrderData]]]:
    """Get sample data for the database."""
    return load_sample_data()
