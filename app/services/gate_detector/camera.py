"""
Camera service implementation.

This module provides functionality for interacting with IP cameras via RTSP.
"""
import cv2
import numpy as np

from app.core.config import settings
from app.core.exceptions import CameraConnectionError, FrameCaptureError
from app.domain.models import CameraCredentials
from app.services.gate_detector.interfaces import CameraService


class OpenCVCameraService(CameraService):
    """Camera service implementation using OpenCV."""

    def get_rtsp_uri(self, credentials: CameraCredentials) -> str:
        """
        Get the RTSP URI for the camera.

        Args:
            credentials: The camera credentials.

        Returns:
            The RTSP URI.
        """
        return credentials.get_rtsp_uri(settings.rtsp_format)

    def capture_frame(self, rtsp_uri: str) -> np.ndarray:
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
        cap = cv2.VideoCapture(rtsp_uri)

        if not cap.isOpened():
            cap.release()
            raise CameraConnectionError("Could not open RTSP stream")

        ret, snapshot = cap.read()
        cap.release()

        if not ret:
            raise FrameCaptureError("Could not read snapshot from RTSP stream")

        return snapshot
