# Politix Connector Hub Backend

A Python backend service that collects and analyzes plenary session protocols and tweets using Mistral AI.

## Features

- Database connection to Supabase for storing plenary session protocols and tweets
- Integration with Mistral AI for LLM-based analysis
- Services for collecting and analyzing data
- FastAPI endpoints for frontend integration

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update with your credentials:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your Supabase and Mistral API credentials

## Database Structure

The application uses two main tables in Supabase:
- `plenary_sessions`: Stores protocols from plenary sessions
- `tweets`: Stores collected tweets

## Running the Application

Start the FastAPI server:

```bash
python -m app.main
```

The API will be available at http://localhost:8000

## Available Services

- Data Collection Service: Periodically collects new data from sources
- Analysis Service: Analyzes collected data using Mistral AI
- API Service: Provides endpoints for the frontend

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 