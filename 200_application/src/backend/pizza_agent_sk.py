"""
Pizza agent module using Semantic Kernel with AzureAIAgent for handling pizza-related AI interactions.
Provides a specialized AI assistant that focuses exclusively on pizza-related queries.
"""
import os
import logging
from typing import Dict, Any
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from semantic_kernel.agents import AzureAIAgentThread, AzureAIAgent
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class PizzaAgentSK:
    """
    Class for interacting with the pizza-agent using Semantic Kernel with AzureAIAgent.
    Handles agent initialization, thread management, and message processing.
    """
    
    def __init__(self) -> None:
        """
        Initialize the PizzaAgentSK with Semantic Kernel setup.
        Sets up Azure credentials and creates/retrieves the pizza agent instance.
        """
        load_dotenv()
        
        # Initialize Azure credentials and project client
        self.credential = DefaultAzureCredential()
        self.project_client = AzureAIAgent.create_client(
            credential=self.credential,
            conn_str=os.environ["PROJECT_CONNECTION_STRING"],
        )
        
        try:
            # Look for existing pizza-agent or create new one
            temp_project_client = AIProjectClient.from_connection_string(
                credential=self.credential,
                conn_str=os.environ["PROJECT_CONNECTION_STRING"]
            )
            all_agents = temp_project_client.agents.list_agents().data
         
            agent_definition = next(
                (a for a in all_agents if a.name == "pizza-agent"),
                None
            )
            
            if not agent_definition:
                logger.info("Creating new pizza-agent, agent wasn't found")
                # Create new agent with pizza-specific instructions
                model_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o")
                instructions = (
                    "You are a helpful assistant which answers questions on pizza dough recipies and methods." 
                    "You politely refuse to talk about any other topic."
                )
                
                agent_definition = self.project_client.agents.create_agent(
                    model=model_name,
                    name="pizza-agent",
                    instructions=instructions
                )
                logger.info(f"Created new pizza-agent with ID: {agent_definition.id}")
            else:
                logger.info("Using existing pizza-agent")

            self.agent = AzureAIAgent(
                client=self.project_client,
                definition=agent_definition,
            )
            logger.info(f"Initialized pizza-agent with ID: {self.agent.id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize pizza-agent: {e}")
    
    async def process_message(self, message: str, thread_id: str | None = None) -> Dict[str, Any]:
        """
        Process a message using the Semantic Kernel pizza agent.
        
        Args:
            message: The user's message to process about pizza-related topics
            thread_id: Optional thread ID for maintaining conversation context
            
        Returns:
            Dict[str, Any]: Response object containing:
                - status: "success" or "error"
                - message: The agent's response text
                - thread_id: Conversation thread identifier
            
        Raises:
            Exception: If message processing fails
        """
        try:
            # Create or reuse conversation thread
            thread = AzureAIAgentThread(
                client=self.project_client,
                thread_id=thread_id,
            )
            logger.info(f"Processing message at agent {self.agent.id} with thread {thread_id}")
            response = await self.agent.get_response(messages=[message], thread=thread)
            logger.info(f"Received response")

            return {
                "status": "success",
                "message": response.content.content,
                "thread_id": response.thread.id
            }
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return {
                "status": "error",
                "message": str(e),
                "thread_id": thread_id
            }