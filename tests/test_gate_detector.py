import pytest
import numpy as np
from unittest.mock import patch, MagicMock

import cv2
from gate_detector import (
    get_rtsp_uri,
    capture_frame,
    detect_gate_status,
    check_gate_status,
    DEFAULT_RTSP_FORMAT
)

class TestGateDetector:
    def test_get_rtsp_uri(self):
        """Test the RTSP URI construction function"""
        # Test with default port
        uri = get_rtsp_uri("user", "pass", "192.168.1.100")
        expected = DEFAULT_RTSP_FORMAT.format(
            username="user",
            password="pass",
            ip_address="192.168.1.100",
            port=554
        )
        assert uri == expected

        # Test with custom port
        uri = get_rtsp_uri("user", "pass", "192.168.1.100", 8554)
        expected = DEFAULT_RTSP_FORMAT.format(
            username="user",
            password="pass",
            ip_address="192.168.1.100",
            port=8554
        )
        assert uri == expected

    @patch('gate_detector.cv2.VideoCapture')
    def test_capture_frame_success(self, mock_video_capture):
        """Test successful frame capture"""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap

        # Call function
        result = capture_frame("rtsp://test")

        # Assertions
        assert result is not None
        assert isinstance(result, np.ndarray)
        assert result.shape == (480, 640, 3)
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_called_once()

    @patch('gate_detector.cv2.VideoCapture')
    def test_capture_frame_cannot_open(self, mock_video_capture):
        """Test frame capture when stream cannot be opened"""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        # Call function
        result = capture_frame("rtsp://test")

        # Assertions
        assert result is None
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_not_called()

    @patch('gate_detector.cv2.VideoCapture')
    def test_capture_frame_read_failure(self, mock_video_capture):
        """Test frame capture when read fails"""
        # Setup mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)
        mock_video_capture.return_value = mock_cap

        # Call function
        result = capture_frame("rtsp://test")

        # Assertions
        assert result is None
        mock_video_capture.assert_called_once_with("rtsp://test")
        mock_cap.release.assert_called_once()

    def test_detect_gate_status_open(self):
        """Test gate status detection for open gate"""
        # Create a mock image with few vertical lines
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw some horizontal lines
        mock_image[100, :] = 255
        mock_image[200, :] = 255

        # Mock HoughLines to return few vertical lines
        with patch('gate_detector.cv2.HoughLines') as mock_hough:
            # Return 5 lines, none of which are vertical
            mock_hough.return_value = np.array([
                [[100, np.pi/2]],  # Horizontal line
                [[200, np.pi/2]],
                [[300, np.pi/2]],
                [[400, np.pi/4]],  # Diagonal line
                [[500, 3*np.pi/4]]
            ])

            result = detect_gate_status(mock_image)
            assert result == "Open"

    def test_detect_gate_status_closed(self):
        """Test gate status detection for closed gate"""
        # Create a mock image
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Mock HoughLines to return many vertical lines
        with patch('gate_detector.cv2.HoughLines') as mock_hough:
            # Return 15 lines, 12 of which are vertical
            vertical_lines = [[[i*10, 0]] for i in range(12)]  # Vertical lines (theta near 0)
            horizontal_lines = [[[i*10, np.pi/2]] for i in range(3)]  # Horizontal lines
            mock_hough.return_value = np.array(vertical_lines + horizontal_lines)

            result = detect_gate_status(mock_image)
            assert result == "Closed"

    def test_detect_gate_status_no_lines(self):
        """Test gate status detection when no lines are detected"""
        # Create a mock image
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Mock HoughLines to return None (no lines detected)
        with patch('gate_detector.cv2.HoughLines') as mock_hough:
            mock_hough.return_value = None

            result = detect_gate_status(mock_image)
            assert result == "Open"

    @patch('gate_detector.get_rtsp_uri')
    @patch('gate_detector.capture_frame')
    @patch('gate_detector.detect_gate_status')
    def test_check_gate_status_success(self, mock_detect, mock_capture, mock_get_uri):
        """Test the main gate status check function - success case"""
        # Setup mocks
        mock_get_uri.return_value = "rtsp://test"
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_capture.return_value = mock_image
        mock_detect.return_value = "Open"

        # Call function
        status, message = check_gate_status("user", "pass", "192.168.1.100")

        # Assertions
        assert status == "Open"
        assert message == "Gate status: Open"
        mock_get_uri.assert_called_once_with("user", "pass", "192.168.1.100", 554)
        mock_capture.assert_called_once_with("rtsp://test")
        mock_detect.assert_called_once_with(mock_image)

    @patch('gate_detector.get_rtsp_uri')
    @patch('gate_detector.capture_frame')
    @patch('gate_detector.detect_gate_status')
    def test_check_gate_status_failure(self, mock_detect, mock_capture, mock_get_uri):
        """Test the main gate status check function - failure case"""
        # Setup mocks
        mock_get_uri.return_value = "rtsp://test"
        mock_capture.return_value = None  # Simulate capture failure

        # Call function
        status, message = check_gate_status("user", "pass", "192.168.1.100")

        # Assertions
        assert status is None
        assert message == "Error: Could not capture snapshot from RTSP stream."
        mock_get_uri.assert_called_once_with("user", "pass", "192.168.1.100", 554)
        mock_capture.assert_called_once_with("rtsp://test")
        mock_detect.assert_not_called()  # Should not be called if capture fails
