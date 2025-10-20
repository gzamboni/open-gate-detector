"""
Custom exceptions for the application.

This module defines custom exceptions that can be raised by the application
and handled appropriately.
"""
# No imports needed for these exception classes


class GateDetectorException(Exception):
    """Base exception for all gate detector exceptions."""

    def __init__(self, message: str):
        """
        Initialize the exception.

        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(self.message)


class CameraConnectionError(GateDetectorException):
    """Exception raised when there is an error connecting to the camera."""

    def __init__(self, message: str = "Error connecting to camera"):
        """
        Initialize the exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class FrameCaptureError(GateDetectorException):
    """Exception raised when there is an error capturing a frame from the camera."""

    def __init__(self, message: str = "Error capturing frame from camera"):
        """
        Initialize the exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class GateDetectionError(GateDetectorException):
    """Exception raised when there is an error detecting the gate status."""

    def __init__(self, message: str = "Error detecting gate status"):
        """
        Initialize the exception.

        Args:
            message: The error message.
        """
        super().__init__(message)
