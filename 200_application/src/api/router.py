"""
API router for handling HTTP requests.
Defines the business logic endpoints of the FastAPI application, including
pizza-related interactions and post processing operations.
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
    """
    Model for pizza-related requests.
    Validates incoming pizza query messages and conversation context.
    """
    message: str          # The user's pizza-related query
    thread_id: str | None = None  # Optional thread ID for maintaining conversation context

@pydantic_dataclass
class PizzaResponse:
    """
    Model for pizza-related responses.
    Structures the AI agent's response and conversation tracking.
    """
    status: str          # Response status ("success" or "error")
    message: str         # The AI agent's response text
    message_id: str | None = None  # Unique ID for this message
    thread_id: str | None = None   # Thread ID for conversation tracking

@dataclass
class PostResponse:
    """
    Model for post-related responses.
    Used by the post processing endpoint.
    """
    status: str          # Processing status
    message: str         # Status or result message 
    timestamp: str       # UTC timestamp of the processing

# Initialize router with tag for API documentation grouping
router = APIRouter(tags=["posts"])

@router.post("/post", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def process_post_request() -> PostResponse:
    """
    Handle POST request for general post processing tasks.
    Currently uses a stub backend for demonstration purposes.
    
    Returns:
        PostResponse: Result of the post processing operation
    """
    service = PostService()
    result = await service.process()
    return PostResponse(**result)

@router.post("/pizza", response_model=PizzaResponse, status_code=status.HTTP_200_OK)
async def process_pizza_request(request: PizzaRequest) -> PizzaResponse:
    """
    Handle pizza-related requests using the AI agent service.
    Maintains conversation context through thread IDs for multi-turn interactions.
    
    Args:
        request: PizzaRequest containing the user's message and optional thread_id
        
    Returns:
        PizzaResponse: The AI agent's response with conversation tracking info
        
    Examples:
        Request: {"message": "How do I make Neapolitan pizza dough?"}
        Response: {
            "status": "success",
            "message": "To make Neapolitan pizza dough...",
            "thread_id": "thread_123..."
        }
    """
    service = PizzaService()
    result = await service.process_message(request.message, request.thread_id)
    return PizzaResponse(**result)