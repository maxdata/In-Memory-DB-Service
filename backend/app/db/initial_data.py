"""Sample data for testing the in-memory database service.

This module and its associated sample_data.json file are intentionally placed in the db/ directory
rather than models/ to maintain proper separation of concerns:

1. Separation of Concerns:
   - Models (in models/) define what entities look like and their behavior
   - Database code (in db/) handles data operations, including seeding/initialization
   - Keeping seed data in db/ maintains this separation

2. Convention:
   - It's a common practice to keep seed/fixture data close to database initialization code
   - Many frameworks (Django, Rails, etc.) follow this pattern
   - Makes it easier for other developers to find initialization data

3. Future Extensions:
   - Additional initialization features (different environments, test data, etc.)
     would naturally fit in the db/ directory
   - Keeps related functionality together
"""

import json
from pathlib import Path
from typing import TypedDict, List, Dict


class UserData(TypedDict):
    id: str
    email: str
    full_name: str
    hashed_password: str
    created_at: str


class OrderData(TypedDict):
    id: str
    user_id: str
    product_name: str
    quantity: int
    total_price: float
    created_at: str


def get_sample_data() -> Dict[str, List[Dict[str, str | int | float]]]:
    """Load sample data from JSON file."""
    json_path = Path(__file__).parent / "sample_data.json"
    with open(json_path) as f:
        data: Dict[str, List[Dict[str, str | int | float]]] = json.load(f)
        return data
