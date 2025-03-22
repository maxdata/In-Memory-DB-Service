# Deployment Guide

This guide covers various deployment scenarios and configurations for the In-Memory Database Service.

## Quick Start

```bash
# From the deploy directory
docker-compose up -d
```

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

## Logging

Docker logging is configured with:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

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