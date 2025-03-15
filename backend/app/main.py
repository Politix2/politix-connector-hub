#!/usr/bin/env python3
"""
Main FastAPI application for the political analysis system.
"""

import asyncio
import os
import sys
from datetime import datetime

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.router import router
from app.config import API_HOST, API_PORT, validate_config
from app.services.scheduler import scheduler

# Load environment variables
load_dotenv()

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")


# Create FastAPI app
app = FastAPI(
    title="Political Analysis API",
    description="API for analyzing political content from plenary sessions and social media",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": "Political Analysis API",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and Docker healthchecks."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
