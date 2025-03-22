# syntax=docker/dockerfile:1

# Stage 1: Build stage
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build/

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Set environment variables for build
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy application code
COPY ./app /build/app/
COPY ./scripts /build/scripts/

# Stage 2: Development stage
FROM builder as development

# Set development environment
ENV ENVIRONMENT=development
ENV DEBUG=true

# Copy all files from builder
COPY --from=builder /build /app/
WORKDIR /app/

# Development command
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: Production stage
FROM python:3.11-slim as production

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set production environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV WORKERS=4

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app/

# Copy only necessary files from builder
COPY --from=builder --chown=appuser:appuser /build/app /app/app/
COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv/

# Set PATH to include virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Set resource limits
ENV MEMORY_LIMIT=512m
ENV CPU_LIMIT=1.0

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Production command with Gunicorn
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
