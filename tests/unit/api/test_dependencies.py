"""
Tests for API dependencies.

This module contains tests for the API dependency injection functions.
"""
import pytest

from app.api.dependencies import get_gate_detector_service, set_gate_detector_service_for_testing
from app.services.gate_detector.detector import OpenCVGateDetectorService
from app.services.gate_detector.interfaces import GateDetectorService


class TestDependencies:
    """Tests for API dependencies."""

    def test_get_gate_detector_service_default(self):
        """Test that get_gate_detector_service returns a default service when no mock is set."""
        # Reset any previously set mock
        set_gate_detector_service_for_testing(None)

        # Get the service
        service = get_gate_detector_service()

        # Verify it's the default implementation
        assert isinstance(service, OpenCVGateDetectorService)

    def test_get_gate_detector_service_mock(self):
        """Test that get_gate_detector_service returns the mock service when set."""
        # Create a mock service
        from unittest.mock import MagicMock
        mock_service = MagicMock(spec=GateDetectorService)

        # Set the mock
        set_gate_detector_service_for_testing(mock_service)

        # Get the service
        service = get_gate_detector_service()

        # Verify it's the mock
        assert service is mock_service

        # Clean up
        set_gate_detector_service_for_testing(None)
