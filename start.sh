#!/bin/sh
set -e

# Default to port 8000 if not set
PORT="${PORT:-8000}"

# Start Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
