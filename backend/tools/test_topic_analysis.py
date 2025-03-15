#!/usr/bin/env python3
"""
Test script for the topic analyzer.
This script takes a topic ID as input and runs the analysis.
"""

import json
import os
import sys

from dotenv import load_dotenv
from loguru import logger

# Add the parent directory to the Python path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.topic_analyzer import TopicAnalyzer

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Load environment variables
load_dotenv()


def main():
    """
    Main function to test the topic analyzer.
    """
    if len(sys.argv) < 2:
        logger.error("Please provide a topic ID as the first argument")
        logger.info("Usage: python test_topic_analysis.py <topic_id>")
        sys.exit(1)

    topic_id = sys.argv[1]
    logger.info(f"Testing topic analysis for topic ID: {topic_id}")

    try:
        # Initialize the topic analyzer
        analyzer = TopicAnalyzer()

        # Try to get topic details first to verify it exists
        try:
            topic = analyzer.fetch_topic_details(topic_id)
            logger.info(f"Found topic: {topic['name']}")
        except ValueError as e:
            logger.error(f"Topic not found: {e}")
            logger.info("Available topics:")

            # List available topics from the database for reference
            try:
                from app.db import db

                topics = db.get_topics()
                for t in topics:
                    logger.info(f"- ID: {t.id}, Name: {t.name}")
            except Exception as list_err:
                logger.error(f"Could not list topics: {list_err}")

            sys.exit(1)

        # Fetch sample data
        sessions = analyzer.fetch_plenary_sessions(limit=5)
        logger.info(f"Fetched {len(sessions)} plenary sessions")

        tweets = analyzer.fetch_tweets(limit=10)
        logger.info(f"Fetched {len(tweets)} tweets")

        # Run the analysis
        logger.info("Running analysis...")
        result = analyzer.analyze_topic(topic_id)

        if result:
            logger.info("Analysis completed successfully!")
            logger.info(f"Summary: {result.get('summary', 'No summary available')}")
            logger.info(
                f"Sentiment: {result.get('sentiment', 'No sentiment available')}"
            )
            logger.info(f"Analysis stored with ID: {result.get('id', 'Unknown')}")

            # Pretty print the analysis data
            if "analysis_data" in result:
                logger.info("\nAnalysis Data:")
                logger.info(json.dumps(result["analysis_data"], indent=2))
        else:
            logger.error("Analysis failed")

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        import traceback

        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
