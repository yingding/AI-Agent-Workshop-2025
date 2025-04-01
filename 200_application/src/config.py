"""
Configuration settings for the application.
Handles loading environment variables and providing settings to the application.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # API Settings
    api_prefix: str = Field("/api", description="API endpoint prefix")
    
    # Health Check Settings
    health_check_token: str = Field(
        "vh7EBWcZq4kP9XmN2sYgT8JH3aRd6MuQ",  # Hardcoded token as requested
        description="Token for health check authentication"
    )
    
    # Telemetry Settings
    enable_telemetry: bool = Field(True, description="Flag to enable/disable telemetry")
    azure_monitor_connection_string: Optional[str] = Field(
        None, 
        description="Connection string for Azure Monitor"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create settings instance
settings = Settings()