# In-Memory Database Service

## Overview

This service provides a production-ready foundation for building RESTful APIs with FastAPI, featuring in-memory data storage and comprehensive testing capabilities. The service supports basic database operations (CRUD) and allows for simple join operations between datasets.

## Documentation

- Project Overview: [README.md](./README.md) - Main project documentation and getting started guide
- Product Requirements: [1_PRODUCT_REQUIREMENTS.md](./1_PRODUCT_REQUIREMENTS.md) - Detailed product specifications and requirements
- Technical Design: [2_TECHNICAL_DESIGN.md](./2_TECHNICAL_DESIGN.md) - System architecture and technical specifications
- Evaluation: [3_EVALUATION.yaml](./3_EVALUATION.yaml) - Detailed code quality, performance, and security assessment criteria
- Backend documentation: [backend/README.md](./backend/README.md) - Implementation details and backend architecture
- API Documentation: Available at `/docs` when the service is running - Interactive API reference
- Deployment guide: [deploy/README.md](./deploy/README.md) - Instructions for deployment and operations
- Contributing Guide: [4_CONTRIBUTING.md](./4_CONTRIBUTING.md) - Guidelines for contributing to the project

## Features

- **FastAPI-based RESTful API**: Production-ready service with well-structured endpoints
- **In-Memory Data Storage**: Utilizes Python dictionaries for efficient data storage and retrieval
- **Data Models**: Implements Pydantic models for robust data validation
- **CRUD Operations**: Complete support for Create, Read, Update, and Delete operations
- **Join Functionality**: Supports joining two datasets based on common keys
- **Comprehensive Testing**: Includes unit tests covering all endpoints and edge cases
- **Docker Support**: Fully containerized application for easy deployment
- **Make Commands**: Unified interface for all development operations

## Project Structure

```
in-memory-db-service/
├── backend/               # Main application code
│   ├── app/              # FastAPI application
│   ├── tests/            # Test suite
│   ├── scripts/          # Utility scripts
│   └── Dockerfile        # Application container definition
├── deploy/               # Deployment configurations
├── Makefile             # Unified command interface
└── README.md            # Project documentation
```

## Technical Capabilities

### Advanced Python & FastAPI Development
- Production-grade FastAPI implementation with async operations
- Comprehensive data validation using Pydantic models
- Type hints and modern Python features utilization
- Clean architecture with separation of concerns

### System Design & Architecture
- Efficient in-memory database implementation with thread-safety considerations
- Well-structured API design with versioning and proper status codes
- Optimized data structures for storage and retrieval
- Scalable architecture with performance considerations

### Testing & Quality Assurance
- Comprehensive test suite using pytest
- Integration tests for API endpoints
- Performance testing for data operations
- 100% test coverage for critical components

### Container & Infrastructure
- Docker Compose setup for development environment
- Health check implementations
- Production-ready container configurations

### Monitoring & Observability
- Structured logging implementation
- Performance tracking endpoints
- Error tracking and reporting

### Documentation & Best Practices
- OpenAPI (Swagger) documentation
- Comprehensive inline documentation
- PEP 8 compliant codebase
- Clear architectural decision records


## Quick Start

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git
- Make

### Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/in-memory-db-service.git
cd in-memory-db-service
```

2. View available commands:
```bash
make help
```

3. Quick development setup:
```bash
make dev  # Installs dependencies, formats code, runs linter and tests, starts the server
```

### Common Make Commands

```bash
make install      # Install dependencies
make test        # Run all tests
make lint        # Run linter
make format      # Format code
make clean       # Clean up temporary files
make run         # Run the application locally
make docker-build # Build Docker image
make docker-run  # Run Docker container
```

## API Documentation

Once the service is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/data/{table}` - Create a new record in a table
- `GET /api/v1/data/{table}/{id}` - Retrieve a record by ID
- `PUT /api/v1/data/{table}/{id}` - Update a record
- `DELETE /api/v1/data/{table}/{id}` - Delete a record
- `GET /api/v1/join/{table1}/{table2}/{key}` - Join two tables on a common key

### API Examples

#### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/data/users" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email": "john.doe@example.com",
      "full_name": "John Doe",
      "age": 30,
      "password": "securepass123"
    }
  }'
```

#### Create an Order
```bash
curl -X POST "http://localhost:8000/api/v1/data/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "product_name": "Widget Pro",
      "quantity": 2,
      "total_price": 99.99,
      "user_id": "USER_ID_HERE"
    }
  }'
```

#### Update a Record
```bash
curl -X PUT "http://localhost:8000/api/v1/data/users/USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "full_name": "John Smith Doe"
    }
  }'
```

#### Join Tables
```bash
curl -X GET "http://localhost:8000/api/v1/join/users/orders/user_id"
```

#### Dump Table Contents
```bash
curl -X GET "http://localhost:8000/api/v1/dump/users"
```

## Development

### Code Quality

The project uses several tools to maintain code quality, all accessible via Make commands:

```bash
make format  # Runs Black code formatter
make lint    # Runs Flake8 for style checking
```

### Running Tests

```bash
make test  # Runs all tests
```

## Deployment

For detailed deployment instructions, see [deploy/README.md](./deploy/README.md).

### Quick Deployment

```bash
make docker-build  # Build the Docker image
make docker-run   # Run the container
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- FastAPI framework and community
- Python community
- All contributors to this project