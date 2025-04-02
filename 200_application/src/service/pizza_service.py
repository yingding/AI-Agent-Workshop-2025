"""
Service layer for pizza-related operations.
Handles business logic between API and pizza agent.
"""
from typing import Dict, Any
import logging

from src.backend.pizza_agent import PizzaAgent
from src.backend.pizza_chat_sk import PizzaChatSK
from src.config import settings

logger = logging.getLogger(__name__)

class PizzaService:
    """Service for handling pizza-related operations."""
    
    def __init__(self) -> None:
        """Initialize the PizzaService with appropriate backend."""
        if settings.use_semantic_kernel:
            logger.info("Initializing with Semantic Kernel backend")
            self.agent = PizzaChatSK()
        else:
            logger.info("Initializing with Azure AI Agent backend")
            self.agent = PizzaAgent()
        
    async def process_message(self, message: str, thread_id: str | None = None) -> Dict[str, Any]:
        """
        Process a pizza-related message by delegating to the selected backend.
        
        Args:
            message: The user's message to process
            thread_id: Optional thread ID for continuing an existing conversation
            
        Returns:
            Dict[str, Any]: Response from the backend including thread_id/conversation_id
        """
        logger.info(f"Processing pizza request with thread_id: {thread_id}")
        return await self.agent.process_message(message, thread_id if not settings.use_semantic_kernel else None)