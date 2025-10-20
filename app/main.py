"""
Main application module.

This module initializes and configures the FastAPI application.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_exception_handlers
from app.api.routes import gate, health
from app.core.config import settings


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        The configured FastAPI application.
    """
    # Create FastAPI app
    fastapi_app = FastAPI(
        title="Gate Status API",
        description="API to check if a gate is open or closed",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.debug
    )

    # Add CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(fastapi_app)

    # Include routers
    fastapi_app.include_router(gate.router)
    fastapi_app.include_router(health.router)

    return fastapi_app


app = create_application()


if __name__ == "__main__":
    # If HOST environment variable is not set, we need to raise an error
    if settings.host is None:
        raise ValueError("HOST environment variable must be set")

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
