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
├── backend/                # Main service implementation
│   ├── app/               # FastAPI application code
│   ├── tests/             # Test suite
│   └── scripts/           # Utility scripts
├── deploy/                # Deployment and infrastructure
├── .github/               # CI/CD and GitHub configurations
├── Makefile              # Development and build commands
├── 1_PRODUCT_REQUIREMENTS.md    # Product specifications
├── 2_TECHNICAL_DESIGN.md        # System architecture
├── 3_EVALUATION.yaml            # Quality criteria
├── 4_CONTRIBUTING.md            # Contribution guidelines
└── README.md             # Project overview
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