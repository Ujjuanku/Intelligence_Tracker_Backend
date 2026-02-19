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
# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Run the application using the script
CMD ["./start.sh"]
