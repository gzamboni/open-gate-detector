"""
API routes for gate-related endpoints.

This module defines the API routes for gate-related operations.
"""
from fastapi import APIRouter, Depends

from app.api.dependencies import Authenticated, GateDetector
from app.domain.models import CameraCredentials
from app.domain.schemas import GateCheckRequest, GateStatusResponse

router = APIRouter(prefix="/gate", tags=["gate"])


@router.post("/check", response_model=GateStatusResponse)
def check_gate(
    request: GateCheckRequest,
    authenticated: Authenticated,
    gate_detector: GateDetector
):
    """
    Check if the gate is open or closed.

    This endpoint requires:
    - API authentication (Bearer Token from API_TOKEN environment variable)
    - Camera credentials and IP in the request body

    Args:
        request: The gate check request.
        authenticated: Authentication dependency.
        gate_detector: Gate detector service dependency.

    Returns:
        A GateStatusResponse with the gate status and a message.
    """
    # Convert request model to domain model
    credentials = CameraCredentials(
        username=request.username,
        password=request.password,
        ip_address=request.ip_address,
        port=request.port if request.port is not None else 554
    )

    # Check gate status
    result = gate_detector.check_gate_status(credentials)

    # Convert domain model to response model
    return GateStatusResponse(
        status=result.status.value if result.status else None,
        message=result.message
    )
