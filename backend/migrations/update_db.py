#!/usr/bin/env python3
"""
Script to update the Supabase database schema.
This script provides instructions for updating the database tables.
"""

import os
import sys

from dotenv import load_dotenv
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing Supabase configuration. Please check your .env file.")
    sys.exit(1)


def main():
    """
    Main function to inform the user how to run the database updates.
    """
    logger.info("Database Update Helper")
    logger.info("=" * 50)
    logger.info("To update the topic_analyses table in your Supabase database:")
    logger.info(
        "1. Log into your Supabase dashboard at: "
        + SUPABASE_URL.replace("https://", "https://app.supabase.com/project/")
    )
    logger.info("2. Go to the SQL Editor section")
    logger.info("3. Create a new query")
    logger.info("4. Copy the SQL below:")

    try:
        # Read the SQL file
        with open(
            os.path.join(os.path.dirname(__file__), "update_topic_analyses.sql"), "r"
        ) as f:
            sql = f.read()

        logger.info("\n" + "=" * 50)
        logger.info("SQL to run:")
        logger.info(sql)
        logger.info("=" * 50)

        logger.info("\n5. Paste the SQL into the editor")
        logger.info("6. Run the query")

    except FileNotFoundError:
        logger.error("Could not find update_topic_analyses.sql file")
        sys.exit(1)


if __name__ == "__main__":
    main()
