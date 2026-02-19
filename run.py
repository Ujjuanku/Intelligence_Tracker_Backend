import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable, default to 8000
    # This avoids shell expansion issues in Docker/Railway
    port = int(os.environ.get("PORT", 8000))
    
    # Run Uvicorn programmatically
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
