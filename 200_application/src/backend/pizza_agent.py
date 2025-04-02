"""
Pizza agent module for handling pizza-related AI interactions.
"""
import os
import logging
from typing import Dict, Any
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ThreadMessage, MessageRole
from dotenv import load_dotenv
import json

logger = logging.getLogger(__name__)

class PizzaAgent:
    """Class for interacting with the pizza-agent AI model."""
    
    def __init__(self) -> None:
        """Initialize the PizzaAgent with Azure AI project client."""
        load_dotenv()
        
        # Initialize Azure credentials and client
        self.credential = DefaultAzureCredential()
        self.project_client = AIProjectClient.from_connection_string(
            credential=self.credential,
            conn_str=os.environ["PROJECT_CONNECTION_STRING"]
        )
        
        # Initialize agent-specific attributes
        self.agent = None
        self.thread = None
        self._initialize_agent()
    
    def _initialize_agent(self) -> None:
        """Initialize or retrieve the pizza-agent."""
        try:
            # Look for existing pizza-agent
            all_agents = self.project_client.agents.list_agents().data
            self.agent = next(
                (a for a in all_agents if a.name == "pizza-agent"),
                None
            )
            
            if not self.agent:
                logger.info("Creating new pizza-agent, agent wasn't found")
                # Create new agent if it doesn't exist
                model_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4")
                instructions = (
                    "You are a helpful assistant which answers questions on pizza dough recipies and methods." 
                    "You politely refuse to talk about any other topic."
                )
                
                self.agent = self.project_client.agents.create_agent(
                    model=model_name,
                    name="pizza-agent",
                    instructions=instructions
                )
                logger.info(f"Created new pizza-agent with ID: {self.agent.id}")
            else:
                logger.info("Using existing pizza-agent")
            
        except Exception as e:
            logger.error(f"Failed to initialize pizza-agent: {e}")
            raise
    
    async def process_message(self, message: str, thread_id: str | None = None) -> Dict[str, Any]:
        """
        Process a message using the pizza-agent.
        
        Args:
            message: The user's message to process
            thread_id: Optional thread ID for continuing an existing conversation
            
        Returns:
            Dict[str, Any]: The agent's response including thread_id
            
        Raises:
            Exception: If message processing fails
        """
        
        try:
            # If thread_id is provided, try to verify it exists
            if thread_id:
                try:
                    # Try to list messages to verify thread exists
                    self.project_client.agents.list_messages(thread_id=thread_id)
                    self.thread = type('Thread', (), {'id': thread_id})()
                    logger.info(f"Using existing thread: {thread_id}")
                except Exception as e:
                    logger.error(f"Thread {thread_id} not found: {e}")
                    return {
                        "status": "error",
                        "message": f"Thread {thread_id} not found",
                        "thread_id": None
                    }
            else:
                # Create new thread if none provided
                self.thread = self.project_client.agents.create_thread()
                logger.info(f"Created new thread: {self.thread.id}")
            
            # Create message in thread
            logger.info(f"Creating new message in thread {self.thread.id}")
            self.project_client.agents.create_message(
                thread_id=self.thread.id,
                role="user",
                content=message
            )
            logger.info("Message created successfully")
            
            # Run the agent
            logger.info(f"Starting agent run with agent_id: {self.agent.id}")
            run = self.project_client.agents.create_and_process_run(
                thread_id=self.thread.id,
                agent_id=self.agent.id
            )
            logger.info(f"Agent run created with run_id: {run.id}")
            
            # Get the response
            logger.info("Retrieving messages from thread")
            messages = self.project_client.agents.list_messages(
                thread_id=self.thread.id
            )
            
            # Log messages
            #logger.info(json.dumps(messages.as_dict(), indent=2))

            #messages = messages.data
            #logger.info(f"Retrieved {len(messages)} messages from thread")

            # Return the latest assistant message
            #agent_messages = [
            #    msg for msg in messages 
            #    if msg.role == MessageRole.AGENT 
            #]
            
            last_agent_msg = messages.get_last_message_by_role(MessageRole.AGENT)

            if last_agent_msg:
                logger.info("Successfully retrieved assistant's response")
                return {
                    "status": "success",
                    "message": last_agent_msg.content[0].text.value,
                    "message_id": last_agent_msg.id,
                    "thread_id": self.thread.id
                }
            else:
                logger.warning("No completed assistant messages found")
                return {
                    "status": "error",
                    "message": "No response received from agent",
                    "thread_id": self.thread.id
                }
                
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return {
                "status": "error",
                "message": str(e),
                "thread_id": getattr(self.thread, 'id', None)
            }