from fastapi import APIRouter

from app.api.v1 import tables

# Create the main API router
api_router = APIRouter(prefix="/api")

# Include versioned routes
v1_router = APIRouter(prefix="/v1")
v1_router.include_router(tables.router)

# Include versioned router in main API router
api_router.include_router(v1_router)
