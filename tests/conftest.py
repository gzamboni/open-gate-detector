"""
Test fixtures for the application.

This module provides fixtures that can be used in tests.
"""
import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.domain.models import CameraCredentials, GateStatus, GateStatusResult
from app.services.gate_detector.interfaces import GateDetectorService


class MockGateDetectorService(GateDetectorService):
    """Mock implementation of the gate detector service for testing."""

    def __init__(self, status=GateStatus.OPEN, error=None):
        """
        Initialize the mock service.

        Args:
            status: The gate status to return.
            error: An error message to return, or None for success.
        """
        self.status = status
        self.error = error
        self.last_credentials = None

    def check_gate_status(self, credentials: CameraCredentials) -> GateStatusResult:
        """
        Mock implementation of check_gate_status.

        Args:
            credentials: The camera credentials.

        Returns:
            A GateStatusResult with the configured status or error.
        """
        # Store the credentials for verification in tests
        self.last_credentials = credentials

        # Return error or success based on configuration
        if self.error:
            return GateStatusResult.error(self.error)
        else:
            return GateStatusResult.success(self.status)


@pytest.fixture(autouse=True)
def mock_cv2_video_capture(monkeypatch):
    """
    Mock cv2.VideoCapture to prevent actual RTSP connections during tests.

    This fixture is automatically used in all tests.
    """
    class MockVideoCapture:
        def __init__(self, *args, **kwargs):
            pass

        def isOpened(self):
            return True

        def read(self):
            # Return a small test image
            import numpy as np
            return True, np.zeros((480, 640, 3), dtype=np.uint8)

        def release(self):
            pass

    monkeypatch.setattr("cv2.VideoCapture", MockVideoCapture)


@pytest.fixture
def test_client():
    """
    Create a test client for the FastAPI application.

    Returns:
        A TestClient instance.
    """
    return TestClient(app)


@pytest.fixture
def mock_gate_detector():
    """
    Create a mock gate detector service and register it with the dependency system.

    This fixture sets up a mock service and ensures it's used by the API.

    Returns:
        A MockGateDetectorService instance.
    """
    from app.api.dependencies import set_gate_detector_service_for_testing

    # Create the mock service
    mock_service = MockGateDetectorService()

    # Register it with the dependency system
    set_gate_detector_service_for_testing(mock_service)

    # Yield the mock for use in tests
    yield mock_service

    # Clean up after the test
    set_gate_detector_service_for_testing(None)


@pytest.fixture
def api_token():
    """
    Get the API token for testing.

    This fixture stores the original token and restores it after the test.

    Returns:
        The API token for testing.
    """
    # Store original token
    original_token = os.environ.get("API_TOKEN")

    # Set a known token for testing
    test_token = "test-token"
    os.environ["API_TOKEN"] = test_token

    yield test_token

    # Restore original token
    if original_token:
        os.environ["API_TOKEN"] = original_token
    else:
        del os.environ["API_TOKEN"]
