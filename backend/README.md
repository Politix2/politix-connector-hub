# Politix Connector Hub Backend

This is the backend service for the Politix Connector Hub, which provides political analysis using Mistral AI and Supabase.

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install mistralai==0.0.7  # Important: Install specific version
   ```

3. Create a `.env` file with the following variables:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. Run the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing CLI Tools

The system includes CLI tools for testing the LLM service and topic analyzer:

1. Test the LLM service:
   ```bash
   python app/services/llm.py
   ```

2. Test the topic analyzer (requires a valid topic ID in the database):
   ```bash
   python app/services/topic_analyzer.py <topic_id> --show-prompt
   ```

## Docker Deployment

### Building the Docker Image

1. Build the image:
   ```bash
   docker build -t politix-backend:latest .
   ```

2. Run locally with environment variables:
   ```bash
   docker run -p 8000:8000 \
     -e MISTRAL_API_KEY=your_mistral_api_key \
     -e SUPABASE_URL=your_supabase_url \
     -e SUPABASE_KEY=your_supabase_key \
     politix-backend:latest
   ```

## Deploying to RunPod

1. Push your Docker image to a registry (Docker Hub, GitHub Container Registry, etc.):
   ```bash
   # Tag your image
   docker tag politix-backend:latest your-registry/politix-backend:latest
   
   # Push to registry
   docker push your-registry/politix-backend:latest
   ```

2. Create a new pod on RunPod:
   - Select a template that includes GPU if needed
   - Set container image to your registry path
   - Add required environment variables:
     - `MISTRAL_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
   - Expose port 8000

3. Start the pod and access your API at the provided URL.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Your API key for Mistral AI | Yes |
| `SUPABASE_URL` | URL for your Supabase project | Yes |
| `SUPABASE_KEY` | API key for Supabase | Yes |

## API Documentation

Once running, the API documentation is available at:
- Swagger UI: `http://your-server:8000/docs`
- ReDoc: `http://your-server:8000/redoc` 