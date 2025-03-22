# Production Dockerfile
FROM python:3.11-slim

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
ENV PYTHONPATH=/app

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app/

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy application code
COPY ./app /app/app/
COPY ./scripts /app/scripts/

# Install production dependencies
RUN pip install --no-cache-dir uvicorn[standard] gunicorn && \
    pip install .

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
