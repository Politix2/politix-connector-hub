#!/bin/bash
set -e

# Print banner
echo "===================================="
echo "Politix Connector Hub Backend Startup"
echo "===================================="

# Check for required environment variables
echo "Checking environment variables..."
required_vars=("MISTRAL_API_KEY" "SUPABASE_URL" "SUPABASE_KEY")
missing_vars=0

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Error: Required environment variable $var is not set"
    missing_vars=1
  else
    echo "✓ $var is set"
  fi
done

if [ $missing_vars -eq 1 ]; then
  echo "Please set the required environment variables and restart the container"
  exit 1
fi

# Apply database migrations if needed
echo "Checking database migrations..."
if [ -f "/workspace/migrations/run_migrations.py" ]; then
  echo "Running database migrations..."
  python /workspace/migrations/run_migrations.py
fi

# Start the application
echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 