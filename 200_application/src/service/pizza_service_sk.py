"""
Service layer for pizza-related operations using Semantic Kernel.
Handles business logic between API and pizza agent.
"""
from typing import Dict, Any
import logging

from src.backend.pizza_agent_sk import PizzaAgentSK

logger = logging.getLogger(__name__)

class PizzaServiceSK:
    """Service for handling pizza-related operations using Semantic Kernel."""
    
    def __init__(self) -> None:
        """Initialize the PizzaServiceSK with Semantic Kernel pizza agent."""
        self.agent = PizzaAgentSK()
        
    async def process_message(self, message: str, conversation_id: str | None = None) -> Dict[str, Any]:
        """
        Process a pizza-related message by delegating to the Semantic Kernel pizza agent.
        
        Args:
            message: The user's message to process
            conversation_id: Optional conversation ID for continuing an existing conversation
            
        Returns:
            Dict[str, Any]: Response from the pizza agent including conversation_id
        """
        logger.info(f"Processing pizza request in SK service layer with conversation_id: {conversation_id}")
        return await self.agent.process_message(message, conversation_id)