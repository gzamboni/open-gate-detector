"""
Security utilities for the application.

This module provides security-related functionality such as authentication.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

# Create a security scheme for Bearer token authentication
security = HTTPBearer(
    scheme_name="Bearer Authentication",
    description="Enter API token as Bearer token",
    auto_error=True
)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """
    Verify the authentication token.

    Args:
        credentials: The HTTP authorization credentials.

    Returns:
        True if the token is valid.

    Raises:
        HTTPException: If the token is invalid.
    """
    # Get the current API token from settings (which reads from environment)
    current_token = settings.api_token

    if credentials.credentials != current_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
