"""Test utility functions for generating test data."""
import random
import string


def random_lower_string(length: int = 32) -> str:
    """Generate a random lowercase string.
    
    Args:
        length: Length of the string to generate. Defaults to 32.
        
    Returns:
        A random string of lowercase letters.
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    """Generate a random email address.
    
    Returns:
        A random email address using the test domain.
    """
    return f"{random_lower_string(10)}@example.com"


def random_order_description() -> str:
    """Generate a random order description.
    
    Returns:
        A random string to use as an order description.
    """
    items = ["Widget", "Gadget", "Device", "Tool", "Component"]
    actions = ["Purchase", "Order", "Buy", "Acquire", "Request"]
    quantities = ["Single", "Bulk", "Multiple", "Set of", "Pack of"]
    
    item = random.choice(items)
    action = random.choice(actions)
    quantity = random.choice(quantities)
    number = random.randint(1, 100)
    
    return f"{action} {quantity} {number} {item}s" 