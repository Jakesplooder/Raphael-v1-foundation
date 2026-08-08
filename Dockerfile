FROM python:3.12-slim

# Install system dependencies, including Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    git \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set up application directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set default environment variables
ENV RAPHAEL_DATA_DIR=/app/data
ENV OLLAMA_URL=http://host.docker.internal:11434
ENV QDRANT_URL=http://qdrant:6333
ENV DASHBOARD_HOST=0.0.0.0

# Command to run RaphaelOS daemon
CMD ["python", "raphael.py", "daemon", "start"]
