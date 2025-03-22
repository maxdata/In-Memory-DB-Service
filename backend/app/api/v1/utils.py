"""API utilities endpoints."""

from fastapi import APIRouter
from typing import Dict

# Create router with prefix and tags
router = APIRouter(prefix="/api/v1/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/ready/")
async def readiness_check() -> Dict[str, str]:
    """Readiness check endpoint."""
    return {"status": "ready"}
