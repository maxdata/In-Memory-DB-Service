"""Main FastAPI application module."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

from .crud import db
from .models import User, Order, UserCreate, OrderCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and clean up the database."""
    # Initialize database tables
    db.clear_table("users")
    db.clear_table("orders")
    yield
    # Clean up database
    db.clear_table("users")
    db.clear_table("orders")

app = FastAPI(
    title="In-Memory Database Service",
    description="A FastAPI service providing in-memory database operations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError):
    """Handle KeyError exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

# API endpoints
@app.post("/api/v1/tables/{table}/records", response_model=Dict[str, Any])
async def add_record(table: str, data: Dict[str, Any]):
    """
    Add a new record to the specified table.
    
    Args:
        table: Name of the table ('users' or 'orders')
        data: Record data to add
        
    Returns:
        The created record
    """
    try:
        record_id = data.get("id")
        if not record_id:
            raise ValueError("Record ID is required")
        return db.add_record(table, record_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tables/{table}/records/{record_id}", response_model=Dict[str, Any])
async def get_record(table: str, record_id: str):
    """
    Get a record from the specified table by ID.
    
    Args:
        table: Name of the table ('users' or 'orders')
        record_id: ID of the record to retrieve
        
    Returns:
        The requested record if found
    """
    record = db.get_record(table, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found in {table}")
    return record

@app.put("/api/v1/tables/{table}/records/{record_id}", response_model=Dict[str, Any])
async def update_record(table: str, record_id: str, data: Dict[str, Any]):
    """
    Update a record in the specified table.
    
    Args:
        table: Name of the table ('users' or 'orders')
        record_id: ID of the record to update
        data: Updated record data
        
    Returns:
        The updated record
    """
    try:
        return db.update_record(table, record_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/v1/tables/{table}/records/{record_id}", response_model=Dict[str, Any])
async def delete_record(table: str, record_id: str):
    """
    Delete a record from the specified table.
    
    Args:
        table: Name of the table ('users' or 'orders')
        record_id: ID of the record to delete
        
    Returns:
        The deleted record
    """
    try:
        return db.delete_record(table, record_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tables/join", response_model=List[Dict[str, Any]])
async def join_tables(table1: str, table2: str, key: str):
    """
    Join two tables based on a common key.
    
    Args:
        table1: Name of the first table
        table2: Name of the second table
        key: Common key to join on
        
    Returns:
        List of joined records
    """
    try:
        return db.join_tables(table1, table2, key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tables/{table}/dump", response_model=List[Dict[str, Any]])
async def dump_table(table: str):
    """
    Dump all contents of the specified table.
    
    Args:
        table: Name of the table to dump
        
    Returns:
        List of all records in the table
    """
    try:
        return db.dump_table(table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
