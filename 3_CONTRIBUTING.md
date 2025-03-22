# Contributing to In-Memory Database Service

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Schema Modifications

### Adding a New Column

1. Locate the model in `backend/app/models.py`
2. Add the new field to the appropriate model class
3. Update validation if needed
4. Update tests to cover the new field

Example:

```python
# Adding a phone_number field to UserBase
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    is_active: bool = Field(True, description="Whether the user is active")
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$', description="User's phone number")
```

### Adding a New Table

1. Create a new model class in `backend/app/models.py`
2. Add the table to the InMemoryDB class
3. Create corresponding CRUD operations
4. Add API endpoints
5. Create tests

Example:

```python
# Adding a new Product table
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)

class Product(ProductBase):
    id: UUID4 = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Update InMemoryDB
class InMemoryDB:
    def __init__(self):
        self.users: Dict[UUID4, User] = {}
        self.orders: Dict[UUID4, Order] = {}
        self.products: Dict[UUID4, Product] = {}  # Add new table
```

### Testing Schema Changes

1. Add unit tests in `backend/tests/`
2. Test data validation
3. Test CRUD operations
4. Test relationships with other tables

Example:

```python
def test_create_product():
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "description": "A test product"
    }
    product = Product(**product_data)
    assert product.name == "Test Product"
    assert product.price == 99.99
```

## Best Practices

1. Always add field descriptions using the Field class
2. Include proper validation rules
3. Use appropriate data types
4. Keep backward compatibility in mind
5. Update documentation when changing schemas
6. Add comprehensive tests for new features

## Documentation

When adding new features or modifying existing ones:

1. Update API documentation
2. Add examples to API_EXAMPLES.md
3. Update README.md if necessary
4. Document any breaking changes

## Need Help?

If you need help with your contribution:

1. Check existing issues and pull requests
2. Create a new issue for discussion
3. Ask for clarification in your pull request
4. Join our community discussions 