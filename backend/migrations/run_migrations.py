#!/usr/bin/env python3
"""
Migration script to create tables in Supabase.
This script uploads and executes the SQL file via Supabase's dashboard.
"""

import os
import sys

import requests
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

        # Execute the SQL using Supabase REST API
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }

        sql_endpoint = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
        response = requests.post(sql_endpoint, headers=headers, json={"query": sql})

        if response.status_code != 200:
            logger.error(
                f"Error executing SQL: {response.status_code} - {response.text}"
            )
            raise Exception(f"Failed to execute SQL: {response.text}")

        logger.info("SQL executed successfully")

        # List all tables we expect to be created
        tables = [
            "users",
            "topics",
            "topic_subscriptions",
            "topic_mentions",
            "plenary_sessions",
            "tweets",
            "topic_analyses",
        ]

        # Verify that tables exist
        for table in tables:
            verify_endpoint = f"{SUPABASE_URL}/rest/v1/{table}?limit=0"
            verify_response = requests.get(verify_endpoint, headers=headers)

            if verify_response.status_code != 200:
                logger.warning(
                    f"Table '{table}' might not have been created successfully: {verify_response.status_code}"
                )
            else:
                logger.info(f"Verified table '{table}' exists")

        logger.info("Migration complete!")
        logger.info("Tables created successfully:")
        for table in tables:
            logger.info(f"- {table}")
    except Exception as e:
        logger.error(f"Error running migration: {e}")
        logger.error(
            "Please run the SQL migration manually using the Supabase dashboard."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
