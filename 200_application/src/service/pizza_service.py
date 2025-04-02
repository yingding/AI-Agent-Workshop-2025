"""
Service layer for pizza-related operations.
Handles business logic between API and pizza agent.
"""
from typing import Dict, Any
import logging

from src.backend.pizza_agent import PizzaAgent

logger = logging.getLogger(__name__)

class PizzaService:
    """Service for handling pizza-related operations."""
    
    def __init__(self) -> None:
        """Initialize the PizzaService with pizza agent."""
        self.agent = PizzaAgent()
        
    async def process_message(self, message: str, thread_id: str | None = None) -> Dict[str, Any]:
        """
        Process a pizza-related message by delegating to the pizza agent.
        
        Args:
            message: The user's message to process
            thread_id: Optional thread ID for continuing an existing conversation
            
        Returns:
            Dict[str, Any]: Response from the pizza agent including thread_id
        """
        logger.info(f"Processing pizza request in service layer with thread_id: {thread_id}")
        return await self.agent.process_message(message, thread_id)