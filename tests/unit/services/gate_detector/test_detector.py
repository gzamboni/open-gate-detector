"""
Tests for the detector service.

This module contains tests for the detector service implementation.
"""
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from app.core.exceptions import GateDetectionError
from app.domain.models import CameraCredentials, GateStatus, GateStatusResult
from app.services.gate_detector.detector import OpenCVDetectionService, OpenCVGateDetectorService


class TestOpenCVDetectionService:
    """Tests for the OpenCVDetectionService."""

    def test_detect_gate_status_open(self):
        """Test gate status detection for open gate."""
        # Create a mock image with few vertical lines
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw some horizontal lines
        mock_image[100, :] = 255
        mock_image[200, :] = 255

        # Create service
        service = OpenCVDetectionService()

        # Mock HoughLines to return few vertical lines
        with patch('cv2.HoughLines') as mock_hough, \
             patch('cv2.cvtColor') as mock_cvt, \
             patch('cv2.Canny') as mock_canny:

            # Setup mocks
            mock_cvt.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_canny.return_value = np.zeros((480, 640), dtype=np.uint8)

            # Return 5 lines, none of which are vertical
            mock_hough.return_value = np.array([
                [[100, np.pi/2]],  # Horizontal line
                [[200, np.pi/2]],
                [[300, np.pi/2]],
                [[400, np.pi/4]],  # Diagonal line
                [[500, 3*np.pi/4]]
            ])

            result = service.detect_gate_status(mock_image)
            assert result == GateStatus.OPEN

    def test_detect_gate_status_closed(self):
        """Test gate status detection for closed gate."""
        # Create a mock image
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Create service
        service = OpenCVDetectionService()

        # Mock HoughLines to return many vertical lines
        with patch('cv2.HoughLines') as mock_hough, \
             patch('cv2.cvtColor') as mock_cvt, \
             patch('cv2.Canny') as mock_canny:

            # Setup mocks
            mock_cvt.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_canny.return_value = np.zeros((480, 640), dtype=np.uint8)

            # Return 15 lines, 12 of which are vertical
            vertical_lines = [[[i*10, 0]] for i in range(12)]  # Vertical lines (theta near 0)
            horizontal_lines = [[[i*10, np.pi/2]] for i in range(3)]  # Horizontal lines
            mock_hough.return_value = np.array(vertical_lines + horizontal_lines)

            result = service.detect_gate_status(mock_image)
            assert result == GateStatus.CLOSED

    def test_detect_gate_status_no_lines(self):
        """Test gate status detection when no lines are detected."""
        # Create a mock image
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Create service
        service = OpenCVDetectionService()

        # Mock HoughLines to return None (no lines detected)
        with patch('cv2.HoughLines') as mock_hough, \
             patch('cv2.cvtColor') as mock_cvt, \
             patch('cv2.Canny') as mock_canny:

            # Setup mocks
            mock_cvt.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_canny.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_hough.return_value = None

            result = service.detect_gate_status(mock_image)
            assert result == GateStatus.OPEN

    def test_detect_gate_status_error(self):
        """Test gate status detection when an error occurs."""
        # Create a mock image
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Create service
        service = OpenCVDetectionService()

        # Mock HoughLines to raise an exception
        with patch('cv2.HoughLines') as mock_hough, \
             patch('cv2.cvtColor') as mock_cvt, \
             patch('cv2.Canny') as mock_canny:

            # Setup mocks
            mock_cvt.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_canny.return_value = np.zeros((480, 640), dtype=np.uint8)
            mock_hough.side_effect = Exception("Test error")

            with pytest.raises(GateDetectionError) as exc_info:
                service.detect_gate_status(mock_image)

            assert "Error detecting gate status: Test error" in str(exc_info.value)


class TestOpenCVGateDetectorService:
    """Tests for the OpenCVGateDetectorService."""

    def test_check_gate_status_success(self):
        """Test the main gate status check function - success case."""
        # Create mock dependencies
        mock_camera_service = MagicMock()
        mock_detection_service = MagicMock()

        # Setup mocks
        mock_camera_service.get_rtsp_uri.return_value = "rtsp://test"
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_camera_service.capture_frame.return_value = mock_image
        mock_detection_service.detect_gate_status.return_value = GateStatus.OPEN

        # Create service with mock dependencies
        service = OpenCVGateDetectorService()
        service.camera_service = mock_camera_service
        service.detection_service = mock_detection_service

        # Create credentials
        credentials = CameraCredentials(
            username="user",
            password="pass",
            ip_address="192.168.1.100"
        )

        # Call function
        result = service.check_gate_status(credentials)

        # Assertions
        assert isinstance(result, GateStatusResult)
        assert result.status == GateStatus.OPEN
        assert result.message == "Gate status: Open"
        mock_camera_service.get_rtsp_uri.assert_called_once_with(credentials)
        mock_camera_service.capture_frame.assert_called_once_with("rtsp://test")
        mock_detection_service.detect_gate_status.assert_called_once_with(mock_image)

    def test_check_gate_status_error(self):
        """Test the main gate status check function - error case."""
        # Create mock dependencies
        mock_camera_service = MagicMock()
        mock_detection_service = MagicMock()

        # Setup mocks to raise an exception
        mock_camera_service.get_rtsp_uri.side_effect = Exception("Test error")

        # Create service with mock dependencies
        service = OpenCVGateDetectorService()
        service.camera_service = mock_camera_service
        service.detection_service = mock_detection_service

        # Create credentials
        credentials = CameraCredentials(
            username="user",
            password="pass",
            ip_address="192.168.1.100"
        )

        # Call function
        result = service.check_gate_status(credentials)

        # Assertions
        assert isinstance(result, GateStatusResult)
        assert result.status is None
        assert "Error checking gate status: Test error" in result.message
        mock_camera_service.get_rtsp_uri.assert_called_once_with(credentials)
        mock_camera_service.capture_frame.assert_not_called()
        mock_detection_service.detect_gate_status.assert_not_called()
