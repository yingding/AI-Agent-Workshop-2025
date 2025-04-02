"""
API router for handling HTTP requests.
This module defines the routes for the FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass

from src.service.post_service import PostService
from src.service.pizza_service import PizzaService

@pydantic_dataclass
class PizzaRequest:
    """Model for pizza-related requests."""
    message: str
    thread_id: str | None = None

@pydantic_dataclass
class PizzaResponse:
    """Model for pizza-related responses."""
    status: str
    message: str
    message_id: str | None = None
    thread_id: str | None = None

@dataclass
class PostResponse:
    """Model for post-related responses."""
    status: str
    message: str
    timestamp: str

# Initialize router
router = APIRouter(tags=["posts"])

@router.post("/post", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def process_post_request() -> PostResponse:
    """
    Handle POST request and delegate to service layer.
    
    Returns:
        PostResponse: Response from the service layer
    """
    service = PostService()
    result = await service.process()
    return PostResponse(**result)

@router.post("/pizza", response_model=PizzaResponse, status_code=status.HTTP_200_OK)
async def process_pizza_request(request: PizzaRequest) -> PizzaResponse:
    """
    Handle pizza-related requests and delegate to the pizza service.
    
    Args:
        request: The pizza request containing the user's message and optional thread_id
        
    Returns:
        PizzaResponse: Response from the pizza service including thread_id for conversation continuity
    """
    service = PizzaService()
    result = await service.process_message(request.message, request.thread_id)
    return PizzaResponse(**result)