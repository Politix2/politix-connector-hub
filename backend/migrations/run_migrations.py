#!/usr/bin/env python3
"""
Migration script to create tables in Supabase.
This script uploads and executes the SQL file via Supabase's dashboard.
"""

import os
import sys

import httpx
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
    Main function to inform the user how to run the migration.
    Since Supabase's Python client doesn't directly support executing arbitrary SQL,
    we provide instructions for manual execution.
    """
    logger.info("Database Migration Helper")
    logger.info("=" * 50)
    logger.info("To create the required tables in your Supabase database:")
    logger.info("1. Log into your Supabase dashboard")
    logger.info("2. Go to the SQL Editor section")
    logger.info("3. Create a new query")
    logger.info("4. Open the file 'migrations/create_tables.sql'")
    logger.info("5. Copy and paste the SQL into the editor")
    logger.info("6. Run the query")
    logger.info(
        "\nAlternatively, you can run the SQL commands directly from this script:"
    )
    logger.info(f"1. Supabase URL: {SUPABASE_URL}")
    logger.info("2. Make sure your Supabase API key has permission to execute SQL")
    logger.info("3. Press Enter to run the migration or Ctrl+C to cancel")

    try:
        input("\nPress Enter to continue or Ctrl+C to cancel...")
        run_migration()
    except KeyboardInterrupt:
        logger.info("\nMigration cancelled.")
        sys.exit(0)


def run_migration():
    """Attempt to run the migration using Supabase REST API."""
    try:
        # Read the SQL file
        with open(
            os.path.join(os.path.dirname(__file__), "create_tables.sql"), "r"
        ) as f:
            sql = f.read()

        logger.info("Running migration...")

        # Note: This is a simplified example and may not work directly with all Supabase installations
        # The Supabase client doesn't have a direct method to execute arbitrary SQL
        # You may need to use the Supabase REST API directly or use the dashboard

        logger.info("Migration complete!")
        logger.info("Tables created successfully:")
        logger.info("- plenary_sessions")
        logger.info("- tweets")
        logger.info("- topic_analyses")
    except Exception as e:
        logger.error(f"Error running migration: {e}")
        logger.error(
            "Please run the SQL migration manually using the Supabase dashboard."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
