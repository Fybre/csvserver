FROM python:3.12-slim

# Set working directory
WORKDIR /app

# System dependencies (optional but useful for csv/file handling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

# Create data and static directories with proper permissions
RUN mkdir -p /app/app/data /app/app/static && chmod -R 755 /app/app

# Expose FastAPI’s default port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
