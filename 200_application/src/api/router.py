"""
API router for handling HTTP requests.
This module defines the routes for the FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from src.service.post_service import PostService

# Initialize router
router = APIRouter(tags=["posts"])

@router.post("/post", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def process_post_request() -> Dict[str, Any]:
    """
    Handle POST request and delegate to service layer.
    
    Returns:
        Dict[str, Any]: Response from the service layer
    """
    service = PostService()
    return await service.process()