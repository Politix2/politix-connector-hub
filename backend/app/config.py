import os

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Application configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Data collection configuration
COLLECTION_INTERVAL_MINUTES = int(os.getenv("COLLECTION_INTERVAL_MINUTES", "60"))
ANALYSIS_INTERVAL_MINUTES = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", "120"))


# Validate required configuration
def validate_config():
    missing_vars = []
    if not SUPABASE_URL:
        missing_vars.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing_vars.append("SUPABASE_KEY")
    if not MISTRAL_API_KEY:
        missing_vars.append("MISTRAL_API_KEY")

    if missing_vars:
        logger.error(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        logger.error("Please set these variables in your .env file")
        return False
    return True
