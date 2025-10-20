"""
API routes for health check endpoints.

This module defines the API routes for health check operations.
"""
from fastapi import APIRouter

from app.domain.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Simple health check endpoint.

    This endpoint can be used to verify that the API is running.

    Returns:
        A HealthResponse with the status "healthy".
    """
    return HealthResponse(status="healthy")
