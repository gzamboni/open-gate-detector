"""
Tests for API error handlers.

This module contains tests for the API error handlers.
"""
import pytest
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.api.errors import (
    gate_detector_exception_handler,
    camera_connection_error_handler,
    frame_capture_error_handler,
    gate_detection_error_handler,
    register_exception_handlers
)
from app.core.exceptions import (
    GateDetectorException,
    CameraConnectionError,
    FrameCaptureError,
    GateDetectionError
)


class TestErrorHandlers:
    """Tests for API error handlers."""

    def test_gate_detector_exception_handler(self):
        """Test the gate detector exception handler."""
        # Create a mock request
        request = Request({"type": "http"})

        # Create an exception
        exc = GateDetectorException("Test error")

        # Call the handler - use pytest-asyncio's run_async helper
        import asyncio
        response = asyncio.run(gate_detector_exception_handler(request, exc))

        # Verify the response
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        content = response.body
        assert isinstance(content, bytes)
        content_str = content.decode('utf-8')
        assert '"status":null' in content_str
        assert '"message":"Test error"' in content_str

    def test_camera_connection_error_handler(self):
        """Test the camera connection error handler."""
        # Create a mock request
        request = Request({"type": "http"})

        # Create an exception
        exc = CameraConnectionError("Connection error")

        # Call the handler
        import asyncio
        response = asyncio.run(camera_connection_error_handler(request, exc))

        # Verify the response
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        content = response.body
        assert isinstance(content, bytes)
        content_str = content.decode('utf-8')
        assert '"status":null' in content_str
        assert '"message":"Connection error"' in content_str

    def test_frame_capture_error_handler(self):
        """Test the frame capture error handler."""
        # Create a mock request
        request = Request({"type": "http"})

        # Create an exception
        exc = FrameCaptureError("Frame error")

        # Call the handler
        import asyncio
        response = asyncio.run(frame_capture_error_handler(request, exc))

        # Verify the response
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        content = response.body
        assert isinstance(content, bytes)
        content_str = content.decode('utf-8')
        assert '"status":null' in content_str
        assert '"message":"Frame error"' in content_str

    def test_gate_detection_error_handler(self):
        """Test the gate detection error handler."""
        # Create a mock request
        request = Request({"type": "http"})

        # Create an exception
        exc = GateDetectionError("Detection error")

        # Call the handler
        import asyncio
        response = asyncio.run(gate_detection_error_handler(request, exc))

        # Verify the response
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        content = response.body
        assert isinstance(content, bytes)
        content_str = content.decode('utf-8')
        assert '"status":null' in content_str
        assert '"message":"Detection error"' in content_str

    def test_register_exception_handlers(self):
        """Test registering exception handlers with the app."""
        # Create a mock app
        class MockApp:
            def __init__(self):
                self.exception_handlers = {}

            def add_exception_handler(self, exc_class, handler):
                self.exception_handlers[exc_class] = handler

        app = MockApp()

        # Register handlers
        register_exception_handlers(app)

        # Verify handlers were registered
        assert app.exception_handlers[GateDetectorException] == gate_detector_exception_handler
        assert app.exception_handlers[CameraConnectionError] == camera_connection_error_handler
        assert app.exception_handlers[FrameCaptureError] == frame_capture_error_handler
        assert app.exception_handlers[GateDetectionError] == gate_detection_error_handler
