from fastapi import APIRouter
from app.api.v1 import tables, utils
from typing import Dict

# Create API router
api_router = APIRouter()

# Include routers
api_router.include_router(tables.router)
api_router.include_router(utils.router)
