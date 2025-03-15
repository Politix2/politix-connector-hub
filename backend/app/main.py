import asyncio
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.router import router
from app.config import API_HOST, API_PORT, validate_config
from app.services.scheduler import scheduler

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")


# Create FastAPI app
app = FastAPI(
    title="Politix Connector Hub API",
    description="API for collecting and analyzing plenary sessions and tweets",
    version="1.0.0",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API router
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    # Validate configuration
    if not validate_config():
        logger.error("Invalid configuration. Exiting...")
        sys.exit(1)

    logger.info("Starting application")

    # Start the scheduler
    scheduler.start()

    # Run initial data collection
    try:
        from app.services.collector import collector

        result = await collector.run_collection()
        logger.info(f"Initial data collection complete: {result}")
    except Exception as e:
        logger.error(f"Error in initial data collection: {e}")


@app.on_event("shutdown")
def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down application")

    # Stop the scheduler
    scheduler.stop()


def start():
    """Start the application."""
    uvicorn.run("app.main:app", host=API_HOST, port=API_PORT, reload=True)


if __name__ == "__main__":
    start()
