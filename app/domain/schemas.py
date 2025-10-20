"""
Pydantic schemas for the gate detector application.

These schemas define the structure of data for API requests and responses.
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GateStatusEnum(str, Enum):
    """Enumeration of possible gate statuses for API responses."""
    OPEN = "Open"
    CLOSED = "Closed"


class GateCheckRequest(BaseModel):
    """Request model for gate status check."""
    username: str = Field(..., description="Camera username for authentication")
    password: str = Field(..., description="Camera password for authentication")
    ip_address: str = Field(..., description="IP address of the camera")
    port: Optional[int] = Field(554, description="RTSP port (default: 554)")

    """Request model for gate status check."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "admin",
                "password": "password",
                "ip_address": "192.168.1.100",
                "port": 554
            }
        }
    }


class GateStatusResponse(BaseModel):
    """Response model for gate status."""
    status: Optional[str] = Field(None, description="Gate status (Open, Closed, or null if error)")
    message: str = Field(..., description="Status message or error description")

    """Response model for gate status."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "Open",
                "message": "Gate status: Open"
            }
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Health status of the service")

    """Response model for health check."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy"
            }
        }
    }
