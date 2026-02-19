FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Railway maps it automatically)
EXPOSE 8000

# IMPORTANT: Use sh -c so $PORT expands correctly
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
