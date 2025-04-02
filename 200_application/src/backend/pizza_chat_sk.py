"""
Pizza chat module using Semantic Kernel for handling pizza-related AI interactions.
"""
import os
import logging
from typing import Dict, Any
from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion, AzureAIInferenceChatPromptExecutionSettings
from semantic_kernel.memory import VolatileMemoryStore
from dotenv import load_dotenv
import json

logger = logging.getLogger(__name__)

class PizzaChatSK:
    """Class for interacting with the pizza-chat using Semantic Kernel."""
    
    def __init__(self) -> None:
        """Initialize the PizzaChatSK with Semantic Kernel setup."""
        load_dotenv()
                
        # System prompt for the pizza agent
        self.system_prompt = """You are a helpful assistant which answers questions on pizza dough recipes and methods.
You politely refuse to talk about any other topic.
Base your answers on established pizza-making techniques and best practices."""
    
    async def process_message(self, message: str, conversation_id: str | None = None) -> Dict[str, Any]:
        """
        Process a message using the Semantic Kernel pizza agent.
        
        Args:
            message: The user's message to process
            conversation_id: Optional conversation ID for continuing an existing conversation
            
        Returns:
            Dict[str, Any]: The agent's response including conversation_id
        """
        try:
            # Initialize the Semantic Kernel
            kernel = Kernel()
            
            # Configure Azure OpenAI Chat Completion
            azure_chat_completion = AzureAIInferenceChatCompletion(
                ai_model_id="gpt-4o",
            )

            # Construct the chat history
            chat_history = ChatHistory()
            chat_history.add_system_message(self.system_prompt)
            chat_history.add_user_message(message)

            execution_settings = AzureAIInferenceChatPromptExecutionSettings(
                max_tokens=400,
                temperature=0.7,
                top_p=0.9,
                # extra_parameters={...},    # model-specific parameters
            )
            
            # Get the chat message content
            response = await azure_chat_completion.get_chat_message_content(chat_history, settings=execution_settings)
            
            logger.info(f"Response received:\n{json.dumps(response.to_dict(), indent=2)}")

            return {
                "status": "success",
                "message": response.content,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return {
                "status": "error",
                "message": str(e),
                "conversation_id": conversation_id
            }