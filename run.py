"""
Entry point script for running the application.

This script imports and runs the FastAPI application.
"""
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    """Run the API server."""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
