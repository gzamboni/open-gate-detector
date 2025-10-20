"""
Interfaces for the gate detector service.

This module defines interfaces that gate detector services must implement.
"""
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any

from app.domain.models import CameraCredentials, GateStatus, GateStatusResult


class GateDetectorService(ABC):
    """Interface for gate detector services."""

    @abstractmethod
    def check_gate_status(self, credentials: CameraCredentials) -> GateStatusResult:
        """
        Check the status of a gate using the provided camera credentials.

        Args:
            credentials: The camera credentials.

        Returns:
            A GateStatusResult containing the gate status and a message.
        """
        pass


class CameraService(ABC):
    """Interface for camera services."""

    @abstractmethod
    def get_rtsp_uri(self, credentials: CameraCredentials) -> str:
        """
        Get the RTSP URI for the camera.

        Args:
            credentials: The camera credentials.

        Returns:
            The RTSP URI.
        """
        pass

    @abstractmethod
    def capture_frame(self, rtsp_uri: str) -> Any:
        """
        Capture a frame from the camera.

        Args:
            rtsp_uri: The RTSP URI.

        Returns:
            The captured frame.

        Raises:
            CameraConnectionError: If the camera connection fails.
            FrameCaptureError: If frame capture fails.
        """
        pass


class DetectionService(ABC):
    """Interface for detection services."""

    @abstractmethod
    def detect_gate_status(self, frame) -> GateStatus:
        """
        Detect the status of a gate in a frame.

        Args:
            frame: The frame to analyze.

        Returns:
            The detected gate status.
        """
        pass
