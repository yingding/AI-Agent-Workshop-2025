"""
Main application module for the FastAPI application.
Handles application setup, middleware configuration, and API route registration.
"""
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file as early as possible
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor

# Import our application components
from src.api.router import router
from src.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Application startup complete")
    yield
    # Shutdown logic
    logger.info("Application shutdown initiated")

# Initialize FastAPI application
app = FastAPI(
    title="API Service",
    description="Production-grade API Service with OpenTelemetry integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup OpenTelemetry with Azure Monitor
if settings.enable_telemetry:
    try:
        configure_azure_monitor(
            connection_string=settings.azure_monitor_connection_string,
            service_name="api-service",
        )
        # Instrument FastAPI for telemetry
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry instrumentation with Azure Monitor configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure OpenTelemetry: {e}")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)