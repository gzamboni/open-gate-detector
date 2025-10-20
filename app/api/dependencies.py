"""
API dependencies for dependency injection.

This module defines dependencies that can be injected into API routes.
"""
from typing import Annotated

from fastapi import Depends

from app.core.security import verify_token
from app.services.gate_detector.interfaces import GateDetectorService
from app.services.gate_detector.detector import OpenCVGateDetectorService


# Global variable to hold the service instance for testing
_gate_detector_service_instance = None

def get_gate_detector_service() -> GateDetectorService:
    """
    Get an instance of the gate detector service.

    This dependency allows for easy mocking in tests.

    Returns:
        An instance of a class implementing the GateDetectorService interface.
    """
    global _gate_detector_service_instance
    if _gate_detector_service_instance is not None:
        return _gate_detector_service_instance
    return OpenCVGateDetectorService()

def set_gate_detector_service_for_testing(service: GateDetectorService | None) -> None:
    """
    Set a mock service for testing.

    This function is used in tests to inject a mock service.

    Args:
        service: The mock service to use, or None to reset.
    """
    global _gate_detector_service_instance
    _gate_detector_service_instance = service


# Define common dependencies
Authenticated = Annotated[bool, Depends(verify_token)]
GateDetector = Annotated[GateDetectorService, Depends(get_gate_detector_service)]
