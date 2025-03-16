FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first to leverage Docker cache
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir mistralai==0.0.7

# Copy backend application code 
COPY backend/ ./

# Make startup script executable
RUN chmod +x /workspace/runpod-startup.sh

# Expose port for API
EXPOSE 8000

# Create a non-root user and set permissions
RUN useradd -m -r appuser && \
    chown -R appuser:appuser /workspace
USER appuser

# Set the entrypoint to our startup script
ENTRYPOINT ["/workspace/runpod-startup.sh"]

# Provide a health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1 