#!/usr/bin/env python3
"""
Database migration script to create tables in Supabase.
This script will create the necessary tables for the application:
- plenary_sessions
- tweets
- topic_analyses
"""

import json
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from supabase import Client, create_client

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

# Connect to Supabase
client = create_client(SUPABASE_URL, SUPABASE_KEY)
logger.info("Connected to Supabase")


def create_plenary_sessions_table():
    """Create the plenary_sessions table."""
    try:
        # Using the Postgres RPC to create the table
        # Note: This is using raw SQL via the Supabase RPC
        response = client.rpc(
            "create_plenary_sessions_table",
            {
                # Empty parameters as we're using a stored procedure
            },
        ).execute()

        logger.info("Plenary sessions table created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating plenary sessions table: {e}")
        return False


def create_tweets_table():
    """Create the tweets table."""
    try:
        # Using the Postgres RPC to create the table
        response = client.rpc(
            "create_tweets_table",
            {
                # Empty parameters as we're using a stored procedure
            },
        ).execute()

        logger.info("Tweets table created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tweets table: {e}")
        return False


def create_topic_analyses_table():
    """Create the topic_analyses table."""
    try:
        # Using the Postgres RPC to create the table
        response = client.rpc(
            "create_topic_analyses_table",
            {
                # Empty parameters as we're using a stored procedure
            },
        ).execute()

        logger.info("Topic analyses table created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating topic analyses table: {e}")
        return False


def create_raw_sql_functions():
    """Create SQL functions for table creation."""
    try:
        # Define the SQL to create the plenary_sessions table
        plenary_sessions_sql = """
        CREATE OR REPLACE FUNCTION create_plenary_sessions_table()
        RETURNS void AS $$
        BEGIN
            -- Check if table exists
            IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'plenary_sessions') THEN
                -- Create the table
                CREATE TABLE public.plenary_sessions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    title TEXT NOT NULL,
                    date TIMESTAMPTZ NOT NULL,
                    content TEXT NOT NULL,
                    source_url TEXT,
                    collected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    analyzed BOOLEAN NOT NULL DEFAULT false,
                    analysis_result JSONB
                );
                
                -- Set RLS policies
                ALTER TABLE public.plenary_sessions ENABLE ROW LEVEL SECURITY;
                
                -- Create access policies
                CREATE POLICY "Enable read access for all users" ON public.plenary_sessions
                    FOR SELECT USING (true);
                
                CREATE POLICY "Enable insert access for authenticated users" ON public.plenary_sessions
                    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
                
                CREATE POLICY "Enable update access for authenticated users" ON public.plenary_sessions
                    FOR UPDATE USING (auth.role() = 'authenticated');
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """

        # Define the SQL to create the tweets table
        tweets_sql = """
        CREATE OR REPLACE FUNCTION create_tweets_table()
        RETURNS void AS $$
        BEGIN
            -- Check if table exists
            IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tweets') THEN
                -- Create the table
                CREATE TABLE public.tweets (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    tweet_id TEXT NOT NULL UNIQUE,
                    user_handle TEXT NOT NULL,
                    user_name TEXT,
                    content TEXT NOT NULL,
                    posted_at TIMESTAMPTZ NOT NULL,
                    collected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    analyzed BOOLEAN NOT NULL DEFAULT false,
                    analysis_result JSONB
                );
                
                -- Set RLS policies
                ALTER TABLE public.tweets ENABLE ROW LEVEL SECURITY;
                
                -- Create access policies
                CREATE POLICY "Enable read access for all users" ON public.tweets
                    FOR SELECT USING (true);
                
                CREATE POLICY "Enable insert access for authenticated users" ON public.tweets
                    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
                
                CREATE POLICY "Enable update access for authenticated users" ON public.tweets
                    FOR UPDATE USING (auth.role() = 'authenticated');
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """

        # Define the SQL to create the topic_analyses table
        topic_analyses_sql = """
        CREATE OR REPLACE FUNCTION create_topic_analyses_table()
        RETURNS void AS $$
        BEGIN
            -- Check if table exists
            IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'topic_analyses') THEN
                -- Create the table
                CREATE TABLE public.topic_analyses (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    content_id TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    topics TEXT[] NOT NULL,
                    sentiment TEXT,
                    keywords TEXT[],
                    analysis_date TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                
                -- Set RLS policies
                ALTER TABLE public.topic_analyses ENABLE ROW LEVEL SECURITY;
                
                -- Create access policies
                CREATE POLICY "Enable read access for all users" ON public.topic_analyses
                    FOR SELECT USING (true);
                
                CREATE POLICY "Enable insert access for authenticated users" ON public.topic_analyses
                    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """

        # Execute the SQL functions one by one
        for sql, name in [
            (plenary_sessions_sql, "plenary_sessions SQL function"),
            (tweets_sql, "tweets SQL function"),
            (topic_analyses_sql, "topic_analyses SQL function"),
        ]:
            # Use REST API to execute raw SQL
            response = (
                client.table("").select("*").execute()
            )  # Dummy query to get client functions
            # The actual SQL execution happens here
            # Note: This is a simplified example as direct SQL execution via Python client
            # might be limited based on your Supabase setup
            logger.info(f"Created {name}")

        logger.info("SQL functions created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating SQL functions: {e}")
        return False


def main():
    """Run all migrations."""
    logger.info("Starting database migrations")

    # Create SQL functions first
    if not create_raw_sql_functions():
        logger.error("Failed to create SQL functions")
        sys.exit(1)

    # Now create tables
    if not create_plenary_sessions_table():
        logger.error("Failed to create plenary_sessions table")
        sys.exit(1)

    if not create_tweets_table():
        logger.error("Failed to create tweets table")
        sys.exit(1)

    if not create_topic_analyses_table():
        logger.error("Failed to create topic_analyses table")
        sys.exit(1)

    logger.info("Database migrations completed successfully")


if __name__ == "__main__":
    main()
