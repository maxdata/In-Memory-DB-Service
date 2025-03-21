# In-Memory Database API Examples

This document provides examples of how to interact with the in-memory database API using curl commands.

## Table Operations

### 1. Add Record

#### Add a User
```bash
curl -X POST "http://localhost:8000/api/v1/data/users" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "email": "john@example.com",
         "full_name": "John Doe",
         "password": "secretpass123"
       }
     }'
```

Example Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2024-03-21T12:00:00"
}
```

#### Add an Order
```bash
curl -X POST "http://localhost:8000/api/v1/data/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "product_name": "Widget Pro",
         "quantity": 5,
         "price": 29.99,
         "user_id": "550e8400-e29b-41d4-a716-446655440000"
       }
     }'
```

Example Response:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "product_name": "Widget Pro",
  "quantity": 5,
  "price": 29.99,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-03-21T12:01:00"
}
```

### 2. Update Record

#### Update a User
```bash
curl -X PUT "http://localhost:8000/api/v1/data/users/550e8400-e29b-41d4-a716-446655440000" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "full_name": "John Smith Doe"
       }
     }'
```

Example Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "full_name": "John Smith Doe",
  "created_at": "2024-03-21T12:00:00"
}
```

#### Update an Order
```bash
curl -X PUT "http://localhost:8000/api/v1/data/orders/660e8400-e29b-41d4-a716-446655440001" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "quantity": 10
       }
     }'
```

Example Response:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "product_name": "Widget Pro",
  "quantity": 10,
  "price": 29.99,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-03-21T12:01:00"
}
```

### 3. Delete Record

#### Delete a User
```bash
curl -X DELETE "http://localhost:8000/api/v1/data/users/550e8400-e29b-41d4-a716-446655440000"
```

Example Response:
```json
{
  "message": "Record deleted successfully from users"
}
```

#### Delete an Order
```bash
curl -X DELETE "http://localhost:8000/api/v1/data/orders/660e8400-e29b-41d4-a716-446655440001"
```

Example Response:
```json
{
  "message": "Record deleted successfully from orders"
}
```

### 4. Join Tables

```bash
curl -X GET "http://localhost:8000/api/v1/join/users/orders/user_id"
```

Example Response:
```json
{
  "data": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "user_email": "john@example.com",
      "user_full_name": "John Smith Doe",
      "order_id": "660e8400-e29b-41d4-a716-446655440001",
      "product_name": "Widget Pro",
      "quantity": 10,
      "price": 29.99,
      "order_created_at": "2024-03-21T12:01:00"
    }
  ],
  "count": 1
}
```

### 5. Dump Table Contents

#### Dump Users Table
```bash
curl -X GET "http://localhost:8000/api/v1/dump/users"
```

Example Response:
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "john@example.com",
      "full_name": "John Smith Doe",
      "created_at": "2024-03-21T12:00:00"
    }
  ],
  "count": 1
}
```

#### Dump Orders Table
```bash
curl -X GET "http://localhost:8000/api/v1/dump/orders"
```

Example Response:
```json
{
  "data": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "product_name": "Widget Pro",
      "quantity": 10,
      "price": 29.99,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2024-03-21T12:01:00"
    }
  ],
  "count": 1
}
```

## Error Responses

### Table Not Found
```json
{
  "detail": "Table invalid_table not found"
}
```

### Record Not Found
```json
{
  "detail": "Record not found"
}
```

### Invalid Data
```json
{
  "detail": "validation error for User\nemail\n  field required"
}
```

### Invalid Join
```json
{
  "detail": "Currently only supports joining users and orders tables"
}
``` 