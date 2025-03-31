"""
Service layer for post processing functionality.
Handles business logic between API and backend layers.
"""
from typing import Dict, Any
import logging

from src.backend.stub1 import Stub1Backend

logger = logging.getLogger(__name__)

class PostService:
    """Service for handling post processing operations."""
    
    def __init__(self) -> None:
        """Initialize the PostService with backend."""
        self.backend = Stub1Backend()
        
    async def process(self) -> Dict[str, Any]:
        """
        Process the post request by delegating to the backend.
        
        Returns:
            Dict[str, Any]: Response from the backend
        """
        logger.info("Processing post request in service layer")
        return await self.backend.process_request()