#!/usr/bin/env python3
"""
Data Importer Tool - Parse files from data directory and import into Supabase plenary_sessions table.
"""

import argparse
import glob
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import dotenv
from loguru import logger

from supabase import Client, create_client

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Load environment variables
dotenv.load_dotenv()


def init_supabase() -> Client:
    """Initialize and return Supabase client."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        logger.error("SUPABASE_URL or SUPABASE_KEY environment variables not set")
        sys.exit(1)

    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        sys.exit(1)


def get_files_from_data_dir() -> List[str]:
    """Get all files from the data directory."""
    data_dir = Path(__file__).parent.parent / "data"

    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return []

    logger.info(f"Scanning directory: {data_dir}")

    # Get all files with common text extensions
    files = []
    for ext in ["*.txt", "*.md", "*.csv", "*.json", "*.xml", "*.*"]:
        files.extend(glob.glob(str(data_dir / ext)))

    # Filter out README and other metadata files
    files = [f for f in files if not os.path.basename(f).lower().startswith("readme")]

    logger.info(f"Found {len(files)} files to process")
    return files


def read_file_content(file_path: str) -> str:
    """Read and return the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
            logger.warning(
                f"File {file_path} was read using latin-1 encoding instead of UTF-8"
            )
            return content
        except Exception as e:
            logger.error(
                f"Error reading file with latin-1 encoding {file_path}: {str(e)}"
            )
            return ""
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return ""


def extract_title_from_content(content: str, default_title: str) -> str:
    """Try to extract a meaningful title from the content."""
    # Try to find a title in the first few lines
    lines = content.split("\n")
    first_lines = [line.strip() for line in lines[:5] if line.strip()]

    for line in first_lines:
        # Check for lines that might be titles (all caps, starts with "TITLE:", etc.)
        if line.isupper() or line.lower().startswith(
            ("title:", "session:", "plenary session:")
        ):
            return (
                line.replace("TITLE:", "")
                .replace("Title:", "")
                .replace("PLENARY SESSION:", "")
                .strip()
            )

    # If we couldn't find a title, use the default
    return default_title


def create_plenary_session_record(file_path: str, content: str) -> Dict[str, Any]:
    """Create a record for the plenary_sessions table."""
    file_name = os.path.basename(file_path)
    current_date = datetime.now().isoformat()

    # Try to extract a better title from the content
    default_title = f"Imported from {file_name}"
    title = extract_title_from_content(content, default_title)

    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "date": current_date,
        "content": content,
        # "source": f"Data import - {file_path}",
        # "imported_at": current_date,
        # "metadata": {
        #     "file_path": file_path,
        #     "file_size": len(content),
        #     "import_date": current_date,
        #     "original_filename": file_name,
        # },
    }


def import_files_to_supabase(dry_run: bool = False) -> int:
    """
    Import all files from data directory to Supabase plenary_sessions table.

    Args:
        dry_run: If True, only simulate the import without actually writing to the database

    Returns:
        Number of successfully processed files
    """
    files = get_files_from_data_dir()
    if not files:
        logger.warning("No files found to import")
        return 0

    success_count = 0
    supabase = None if dry_run else init_supabase()

    for file_path in files:
        logger.info(f"Processing file: {file_path}")
        content = read_file_content(file_path)

        if not content:
            logger.warning(f"Empty or unreadable file: {file_path}")
            continue

        record = create_plenary_session_record(file_path, content)

        if dry_run:
            logger.info(f"[DRY RUN] Would import file: {file_path}")
            logger.info(f"[DRY RUN] Record title: {record['title']}")
            logger.info(
                f"[DRY RUN] Content length: {len(record['content'])} characters"
            )
            success_count += 1
            continue

        try:
            result = supabase.table("plenary_sessions").insert(record).execute()
            if result.data:
                logger.info(f"Successfully imported file: {file_path}")
                success_count += 1
            else:
                logger.error(f"Failed to import file: {file_path}")
        except Exception as e:
            logger.error(f"Error importing file {file_path}: {str(e)}")

    return success_count


def main():
    """Main entry point for the data importer tool."""
    parser = argparse.ArgumentParser(
        description="Import data files into Supabase plenary_sessions table"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate import without writing to database",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

    logger.info(f"Starting data import process{' (DRY RUN)' if args.dry_run else ''}")

    # Check if Supabase is properly configured (unless dry run)
    if not args.dry_run:
        supabase = init_supabase()
        try:
            test_query = (
                supabase.table("plenary_sessions")
                .select("count", count="exact")
                .limit(1)
                .execute()
            )
            logger.info(
                f"Connected to Supabase successfully - table has {test_query.count} records"
            )
        except Exception as e:
            logger.error(f"Error connecting to Supabase: {str(e)}")
            sys.exit(1)

    # Import files
    imported_count = import_files_to_supabase(dry_run=args.dry_run)

    logger.info(
        f"Import process completed. Successfully {'processed' if args.dry_run else 'imported'} {imported_count} files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
