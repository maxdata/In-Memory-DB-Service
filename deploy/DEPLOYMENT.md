# Deployment Guide

## Table of Contents
- [Quick Start](#quick-start)
- [Deployment Architecture](#deployment-architecture)
- [Deployment Scenarios](#deployment-scenarios)
- [Resource Management](#resource-management)
- [Health Checks](#health-checks)
- [Logging](#logging)
- [Documentation](#documentation)
- [Maintenance](#maintenance)
- [Support](#support)

This guide covers various deployment scenarios and configurations for the In-Memory Database Service.

## Quick Start

```bash
# From the deploy directory
docker-compose up -d
```

## Deployment Architecture

### Docker Configuration
The service uses a multi-stage Docker build process optimized for both development and production environments.

#### Multi-Stage Build Architecture
1. **Builder Stage**
   - Python 3.11-slim base image
   - UV package manager (v0.5.11)
   - Build dependencies installation
   - Dependency management with UV sync
   - Bytecode compilation enabled

2. **Development Stage**
   - Inherits from builder
   - Development environment settings
   - Hot-reload with Uvicorn
   - Debug mode enabled
   - Source code mounting

3. **Production Stage**
   - Minimal Python 3.11-slim image
   - Non-root user execution
   - Resource limits:
     - Memory: 512MB
     - CPU: 1.0 cores
   - 4 Gunicorn workers
   - Health check implementation

#### Container Orchestration
Docker Compose configuration includes:
1. Build configuration with target selection
2. Resource management (CPU/memory limits)
3. Environment variable configuration
4. Health monitoring
5. Log rotation
6. Network isolation

#### Deployment File Organization
The deployment configuration follows a structured organization pattern:

```
project_root/
├── backend/
│   └── Dockerfile        # Service build configuration
└── deploy/
    ├── docker-compose.yml    # Orchestration configuration
    └── README.md            # Deployment documentation
```

This organization follows these principles:
1. **Separation of Concerns**
   - `Dockerfile` stays with application code in `backend/` as it defines the service build
   - Deployment orchestration files remain in `deploy/` directory
   - Clear separation between build and deployment configurations

2. **Context Management**
   - Docker Compose uses relative path `context: ../backend` to reference the backend directory
   - This allows running `docker-compose up` from the `deploy` directory while correctly locating the Dockerfile

3. **Maintainability Benefits**
   - Deployment configurations are centralized in one directory
   - Build configurations stay with their respective services
   - Easier to manage multiple deployment configurations
   - Clear separation for version control

4. **Scalability**
   - Easy to add new services with their own Dockerfiles
   - Simple to create different deployment configurations
   - Clear structure for adding deployment-related tools and scripts

## Package Management with UV

UV is the high-performance Python package installer and resolver used in this project. It provides several advantages:

### UV Configuration
- Version: 0.5.11 (in Docker build)
- Bytecode compilation enabled (`UV_COMPILE_BYTECODE=1`)
- Link mode set to copy (`UV_LINK_MODE=copy`)

### Key Features
1. **Dependency Resolution**
   - Fast, reliable dependency resolution
   - Uses `pyproject.toml` and `uv.lock` for dependency management
   - Frozen dependencies with `--frozen` flag for reproducible builds

2. **Development Setup**
   ```bash
   # Install dependencies
   uv sync
   
   # Install in editable mode
   uv install --editable .
   ```

3. **CI/CD Integration**
   - Integrated with GitHub Actions workflows
   - Caching enabled for faster builds
   - Consistent dependency installation across environments

4. **Performance Benefits**
   - Parallel package downloads
   - Optimized dependency resolution
   - Bytecode compilation for faster startup
   - Efficient caching mechanism

### Environment Management
- Development and production environments managed separately
- Virtual environment creation and activation handled automatically
- Consistent package versions across all environments

## Deployment Scenarios

### 1. Local Development

```bash
# Using Docker Compose with development target
export DOCKER_TARGET=development
docker-compose up -d

# Or directly with Docker
docker build -t in-memory-db-service:dev -f backend/Dockerfile --target development .
docker run -d \
  --name in-memory-db-service \
  -p 8000:8000 \
  -e ENVIRONMENT=development \
  -e DEBUG=true \
  in-memory-db-service:dev
```

### 2. Production Deployment

```bash
# Build production image
docker build -t in-memory-db-service:prod -f backend/Dockerfile --target production .

# Run with production settings
docker run -d \
  --name in-memory-db-service \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  -e WORKERS=4 \
  -e CORS_ORIGINS=http://localhost:8000 \
  in-memory-db-service:prod
```

### 3. Environment Variables

The service supports the following environment variables:
- `ENVIRONMENT`: Set to either 'development' or 'production' (default: production)
- `DEBUG`: Enable debug mode (default: false)
- `WORKERS`: Number of worker processes (default: 4)
- `CORS_ORIGINS`: Allowed CORS origins (default: http://localhost:8000)
- `DOCKER_TARGET`: Build target for docker-compose (development/production)

## Resource Management

### Memory and CPU Limits

The service is configured with the following resource limits:
```yaml
limits:
  cpus: '1.0'
  memory: 512M
reservations:
  cpus: '0.25'
  memory: 256M
```

### Monitoring

1. Container Health
   ```bash
   # Check container logs
   docker logs in-memory-db-service
   
   # Monitor resource usage
   docker stats in-memory-db-service
   ```

2. Application Metrics
   - Endpoint response times
   - Memory usage
   - Request/response rates
   - Error rates

## Health Checks

The service includes automated health checks:
```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Health check configuration
interval: 30s
timeout: 5s
retries: 3
start_period: 5s
```

Detailed health check implementation:
- Basic health check endpoint at `/api/v1/utils/health-check`
- Docker health check configuration:
  - 30-second interval
  - 5-second timeout
  - 3 retries
  - 5-second start period

## Logging

Docker logging is configured with:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Documentation

### API Documentation
- Swagger/OpenAPI 3.0 documentation available at `/docs`
- ReDoc alternative documentation at `/redoc`
- Markdown documentation in project repository

### Setup Instructions
Detailed setup instructions are available in the sections above. Key documentation includes:
- Docker configuration and build process
- Environment variable configuration
- Resource management
- Health check setup
- Logging configuration

### Sample API Calls
API examples are available in the Swagger documentation. Common operations include:
- CRUD operations for resources
- Join operations
- Health checks
- System operations

### Troubleshooting Guide
Common issues and solutions:
1. Container fails to start:
   - Check resource limits
   - Verify environment variables
   - Review logs for errors
   
2. Performance issues:
   - Monitor resource usage
   - Check concurrent connections
   - Review logging configuration

3. Health check failures:
   - Verify service connectivity
   - Check resource availability
   - Review health check configuration

## Maintenance

1. Regular Tasks
   - Monitor resource usage
   - Check for memory leaks
   - Update dependencies
   - Backup data regularly

2. Updates and Upgrades
   ```bash
   # Pull latest image
   docker pull in-memory-db-service:latest
   
   # Graceful restart
   docker-compose down
   docker-compose up -d
   ```

## Support

For additional support:
1. Check the issue tracker
2. Join our community discussions
3. Contact the maintainers
4. Review the documentation 