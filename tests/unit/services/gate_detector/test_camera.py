"""
Tests for the camera service.

This module contains tests for the camera service implementation.
"""
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from app.core.config import settings
from app.core.exceptions import CameraConnectionError, FrameCaptureError
from app.domain.models import CameraCredentials
from app.services.gate_detector.camera import OpenCVCameraService


class TestOpenCVCameraService:
    """Tests for the OpenCVCameraService."""

    def test_get_rtsp_uri(self):
        """Test the RTSP URI construction function."""
        # Create service
        service = OpenCVCameraService()

        # Test with default port
        credentials = CameraCredentials(
            username="user",
            password="pass",
            ip_address="192.168.1.100"
        )
        uri = service.get_rtsp_uri(credentials)
        expected = settings.rtsp_format.format(
            username="user",
            password="pass",
            ip_address="192.168.1.100",
            port=554
        )
        assert uri == expected

        # Test with custom port
        credentials = CameraCredentials(
            username="user",
            password="pass",
            ip_address="192.168.1.100",
            port=8554
        )
        uri = service.get_rtsp_uri(credentials)
        expected = settings.rtsp_format.format(
            username="user",
            password="pass",
            ip_address="192.168.1.100",
            port=8554
        )
        assert uri == expected

    @patch('cv2.VideoCapture')
    def test_capture_frame_success(self, mock_video_capture):
        """Test successful frame capture."""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap

        # Create service
        service = OpenCVCameraService()

        # Call function
        result = service.capture_frame("rtsp://test")

        # Assertions
        assert result is not None
        assert isinstance(result, np.ndarray)
        assert result.shape == (480, 640, 3)
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_called_once()

    @patch('cv2.VideoCapture')
    def test_capture_frame_cannot_open(self, mock_video_capture):
        """Test frame capture when stream cannot be opened."""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        # Create service
        service = OpenCVCameraService()

        # Call function and check exception
        with pytest.raises(CameraConnectionError) as exc_info:
            service.capture_frame("rtsp://test")

        assert "Could not open RTSP stream" in str(exc_info.value)
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_called_once()

    @patch('cv2.VideoCapture')
    def test_capture_frame_read_failure(self, mock_video_capture):
        """Test frame capture when read fails."""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)
        mock_video_capture.return_value = mock_cap

        # Create service
        service = OpenCVCameraService()

        # Call function and check exception
        with pytest.raises(FrameCaptureError) as exc_info:
            service.capture_frame("rtsp://test")

        assert "Could not read snapshot from RTSP stream" in str(exc_info.value)
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_called_once()
