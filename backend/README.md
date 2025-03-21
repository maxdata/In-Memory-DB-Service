# In-Memory Database Service - Backend

## Overview

This is the backend implementation of an in-memory database service using FastAPI. The service provides basic database operations (CRUD) and supports join operations between datasets, all while maintaining data in memory using Python dictionaries.

## API Endpoints

The service exposes the following REST endpoints:

* `POST /add_record/{table}` - Add a record to the specified table
* `PUT /update_record/{table}/{record_id}` - Update a record
* `DELETE /delete_record/{table}/{record_id}` - Delete a record
* `GET /join/{table1}/{table2}/{key}` - Join two tables based on a given key

## Development Setup

### Project Structure

* `./app/models.py` - Data models and in-memory storage implementation
* `./app/api/` - API endpoints implementation
* `./app/crud.py` - CRUD operations implementation
* `./tests/` - Unit tests
* `./scripts/` - Development utility scripts

### Quick Start

From the root directory:

```bash
# Install dependencies and start development server
make dev

# Or run individual commands:
make install  # Install dependencies
make format  # Format code
make lint    # Run linter
make test    # Run tests
make run     # Start server
```

## Docker Development

### Starting the Service

```bash
# Build and run with Docker
make docker-build
make docker-run

# The service will be available at http://localhost:8000
```

For an interactive development session:

```bash
docker exec -it in-memory-db-service bash
```

## Testing

### Running Tests

```bash
# From root directory
make test

# With coverage report (from backend directory)
pytest --cov=app --cov-report=term-missing
```

## Data Models

The service uses Python dictionaries for in-memory storage, with the following features:

* Efficient data storage and retrieval
* Support for multiple tables/datasets
* Join operations between datasets
* Data persistence within the application lifecycle

## Development Guidelines

1. Use Pydantic models for data validation
2. Implement comprehensive error handling
3. Follow RESTful API best practices
4. Write unit tests for new functionality
5. Document API changes

## Performance Considerations

* Optimize memory usage for large datasets
* Implement efficient join algorithms
* Consider data structure choice for operations
* Monitor memory consumption during development
