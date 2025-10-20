"""
Gate detector service implementation.

This module provides functionality for detecting gate status using computer vision.
"""
import cv2  # pylint: disable=no-member
import numpy as np

from app.core.config import settings
from app.core.exceptions import GateDetectionError
from app.domain.models import CameraCredentials, GateStatus, GateStatusResult
from app.services.gate_detector.interfaces import GateDetectorService, DetectionService
from app.services.gate_detector.camera import OpenCVCameraService


# pylint: disable=too-few-public-methods
class OpenCVDetectionService(DetectionService):
    """Detection service implementation using OpenCV."""

    def detect_gate_status(self, frame: np.ndarray) -> GateStatus:
        """
        Detect the status of a gate in a frame using the Hough Line Transform.

        Args:
            frame: The frame to analyze.

        Returns:
            The detected gate status.

        Raises:
            GateDetectionError: If gate detection fails.
        """
        # pylint: disable=no-member
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)

            lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

            num_vertical_lines = 0
            if lines is not None:
                for i in range(len(lines)):
                    # Each line is a 1x2 array containing rho and theta
                    # We only need theta for vertical line detection
                    theta = lines[i][0][1]
                    # Filter for vertical lines (theta is close to 0 or pi)
                    if np.abs(theta) < np.pi / 180 * 10 or np.abs(theta - np.pi) < np.pi / 180 * 10:
                        num_vertical_lines += 1

            # Define a threshold for the number of vertical lines
            line_threshold = settings.line_threshold

            if num_vertical_lines > line_threshold:
                return GateStatus.CLOSED
            return GateStatus.OPEN

        except Exception as e:
            raise GateDetectionError(f"Error detecting gate status: {str(e)}") from e


# pylint: disable=too-few-public-methods
class OpenCVGateDetectorService(GateDetectorService):
    """Gate detector service implementation using OpenCV."""

    def __init__(self):
        """Initialize the service with its dependencies."""
        self.camera_service = OpenCVCameraService()
        self.detection_service = OpenCVDetectionService()

    def check_gate_status(self, credentials: CameraCredentials) -> GateStatusResult:
        """
        Check the status of a gate using the provided camera credentials.

        Args:
            credentials: The camera credentials.

        Returns:
            A GateStatusResult containing the gate status and a message.
        """
        try:
            rtsp_uri = self.camera_service.get_rtsp_uri(credentials)
            frame = self.camera_service.capture_frame(rtsp_uri)
            status = self.detection_service.detect_gate_status(frame)

            return GateStatusResult.success(status)

        except Exception as e:  # pylint: disable=broad-exception-caught
            return GateStatusResult.error(str(e))
