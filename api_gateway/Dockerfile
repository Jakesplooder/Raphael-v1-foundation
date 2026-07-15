FROM python:3.12-slim

# Set the working directory to the root of the app
WORKDIR /app

# Install system dependencies (like Tesseract OCR for vision)
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them first to leverage Docker layer caching
COPY api_gateway/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repository into the container
COPY . /app/

# Set the Python path so any script in /app/api_gateway can import raphael_core natively
ENV PYTHONPATH=/app

CMD ["bash"]
