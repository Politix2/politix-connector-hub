#!/usr/bin/env python3
"""
Tool to check if the required tables exist in the Supabase database.
"""

import os
import sys
from typing import Any, Dict, List

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


def check_tables():
    """Check if the required tables exist in the database."""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    # List all tables that should exist
    expected_tables = [
        "users",
        "topics",
        "topic_subscriptions",
        "topic_mentions",
        "plenary_sessions",
        "tweets",
        "topic_analyses",
    ]

    # Try to get schema information using a direct SQL query
    logger.info("Attempting to get database schema information...")

    # SQL to list all tables in the public schema
    list_tables_sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """

    try:
        # Try using PostgREST's rpc endpoint if available
        rpc_endpoint = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
        rpc_payload = {"sql": list_tables_sql}
        rpc_response = requests.post(rpc_endpoint, headers=headers, json=rpc_payload)

        if rpc_response.status_code == 200:
            tables_in_db = [table["table_name"] for table in rpc_response.json()]
            logger.info(f"Tables found in database via RPC: {tables_in_db}")
        else:
            logger.warning(
                f"RPC method failed: {rpc_response.status_code} - {rpc_response.text}"
            )
    except Exception as e:
        logger.warning(f"Error using RPC method: {e}")

    # For each table, try to get 0 rows
    logger.info("Checking if tables exist in the database...")
    missing_tables = []
    existing_tables = []

    for table in expected_tables:
        url = f"{SUPABASE_URL}/rest/v1/{table}?limit=0"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            existing_tables.append(table)
            logger.info(f"Table '{table}' found")
        else:
            missing_tables.append(table)
            logger.warning(
                f"Table '{table}' not found (Status: {response.status_code}, Response: {response.text})"
            )

    # Print summary
    if existing_tables:
        logger.info("\nTables that exist:")
        for table in existing_tables:
            logger.info(f"- {table}")

    if missing_tables:
        logger.warning("\nTables that are missing:")
        for table in missing_tables:
            logger.warning(f"- {table}")

        logger.info("\nPlease run the SQL migration in the Supabase dashboard:")
        logger.info(
            "1. Log into the Supabase dashboard at: "
            + SUPABASE_URL.replace("https://", "https://app.supabase.com/project/")
        )
        logger.info("2. Go to the SQL Editor section")
        logger.info("3. Create a new query")
        logger.info("4. Copy the SQL from migrations/missing_tables.sql")
        logger.info("5. Paste the SQL into the editor")
        logger.info("6. Run the query")
    else:
        logger.info("All tables exist in the database.")

    # Check API key permissions
    logger.info("\nChecking API key permissions...")
    logger.info(f"API Key (first 10 chars): {SUPABASE_KEY[:10]}...")

    # Try to list all permissions for diagnostic purposes
    auth_endpoint = f"{SUPABASE_URL}/auth/v1/token"
    auth_response = requests.get(auth_endpoint, headers=headers)

    if auth_response.status_code == 200:
        logger.info("API key authentication successful")
    else:
        logger.warning(
            f"API key authentication issue: {auth_response.status_code} - {auth_response.text}"
        )


if __name__ == "__main__":
    check_tables()
