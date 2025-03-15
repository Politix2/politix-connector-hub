import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from app.config import ANALYSIS_INTERVAL_MINUTES, COLLECTION_INTERVAL_MINUTES
from app.services.analyzer import analyzer
from app.services.collector import collector


class Scheduler:
    """Service for scheduling periodic tasks."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        logger.info("Scheduler initialized")

    async def collection_job(self):
        """Job to run data collection."""
        logger.info("Running scheduled data collection job")
        try:
            result = await collector.run_collection()
            logger.info(f"Data collection complete: {result}")
        except Exception as e:
            logger.error(f"Error in data collection job: {e}")

    async def analysis_job(self):
        """Job to run data analysis."""
        logger.info("Running scheduled data analysis job")
        try:
            result = await analyzer.run_analysis()
            logger.info(f"Data analysis complete: {result}")
        except Exception as e:
            logger.error(f"Error in data analysis job: {e}")

    def start(self):
        """Start the scheduler."""
        # Schedule data collection job
        self.scheduler.add_job(
            self.collection_job,
            trigger=IntervalTrigger(minutes=COLLECTION_INTERVAL_MINUTES),
            id="data_collection",
            name="Collect Data",
            replace_existing=True,
        )

        # Schedule data analysis job
        self.scheduler.add_job(
            self.analysis_job,
            trigger=IntervalTrigger(minutes=ANALYSIS_INTERVAL_MINUTES),
            id="data_analysis",
            name="Analyze Data",
            replace_existing=True,
        )

        # Start the scheduler
        self.scheduler.start()
        logger.info(
            f"Scheduler started. Collection interval: {COLLECTION_INTERVAL_MINUTES}m, Analysis interval: {ANALYSIS_INTERVAL_MINUTES}m"
        )

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")


# Singleton scheduler
scheduler = Scheduler()
