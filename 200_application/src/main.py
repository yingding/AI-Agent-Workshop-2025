"""
Main application module for the FastAPI application.
Sets up the production-grade API service with OpenTelemetry integration, CORS,
and proper request routing. Configures logging and handles application lifecycle.
"""
import logging
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file as early as possible
# to ensure all settings are available during app initialization
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor

# Import our application components
from src.api.router import router as api_router
from src.infra.router import router as infra_router
from src.config import settings

# Configure logging to use stdout for container-friendly logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
# Reduce noise from Azure HTTP logging
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Lifespan context manager handles startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Place any initialization code that should run before accepting requests here,
    and cleanup code in the finally block.
    """
    # Startup logic
    logger.info("Application startup complete")
    yield
    # Shutdown logic - cleanup resources, close connections, etc.
    logger.info("Application shutdown initiated")

# Initialize FastAPI application with metadata
app = FastAPI(
    title="API Service",
    description="Production-grade API Service with OpenTelemetry integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup OpenTelemetry with Azure Monitor if enabled
if settings.enable_telemetry:
    try:
        configure_azure_monitor(
            connection_string=settings.azure_monitor_connection_string,
            service_name="api-service",
        )
        # Instrument FastAPI for automatic telemetry collection
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry instrumentation with Azure Monitor configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure OpenTelemetry: {e}")

# Include routers for API endpoints and infrastructure endpoints
app.include_router(api_router)    # Business logic endpoints
app.include_router(infra_router)  # System endpoints like health checks

if __name__ == "__main__":
    # Development server configuration
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)