FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for some python packages or potential debugging)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the application
# Run the application (Shell form to allow variable expansion)
CMD /bin/sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
